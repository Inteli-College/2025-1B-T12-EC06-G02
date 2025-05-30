package com.example.sodcontrol.tellocontroller

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.example.sodcontrol.R
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Build
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import com.example.sodcontrol.utils.FileUtils
import androidx.activity.result.contract.ActivityResultContracts
import android.Manifest
import android.widget.Button
import android.widget.Toast
import androidx.activity.result.ActivityResultLauncher
import android.provider.OpenableColumns


class DatabaseSender : AppCompatActivity() {
    private lateinit var pickMediaLauncher: ActivityResultLauncher<String>
    private var selectedImageUri: Uri? = null
    private val STORAGE_PERMISSION_CODE = 101

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.database_send)

        pickMediaLauncher = registerForActivityResult(ActivityResultContracts.GetContent()) { uri: Uri? ->
            if (uri != null) {
                selectedImageUri = uri
                Toast.makeText(this, "Imagem selecionada!", Toast.LENGTH_SHORT).show()

                val fileName = getFileNameFromUri(uri)

                if (fileName != null) {
                    SupabaseClient.uploadImageAndInsertRecord(
                        context = this,
                        localFilePath = FileUtils.getPath(this, uri) ?: "",
                        fileName = fileName
                    )
                    Toast.makeText(this, "Imagem enviada para o banco!", Toast.LENGTH_SHORT).show()
                } else {
                    Toast.makeText(this, "Erro ao obter o nome do arquivo", Toast.LENGTH_SHORT).show()
                }
            } else {
                Toast.makeText(this, "Nenhuma imagem selecionada", Toast.LENGTH_SHORT).show()
            }
        }

        if (!checkStoragePermission()) {
            requestStoragePermission()
        }

        val databaseButton = findViewById<Button>(R.id.btnConnectDatabase)

        databaseButton.setOnClickListener {
            Toast.makeText(this, "Imagem sendo enviada...", Toast.LENGTH_SHORT).show()
            if (checkStoragePermission()) {
                pickMediaLauncher.launch("image/*")
            } else {
                requestStoragePermission()
            }
        }
    }

    private fun getFileNameFromUri(uri: Uri): String? {
        var result: String? = null
        if (uri.scheme == "content") {
            val cursor = contentResolver.query(uri, null, null, null, null)
            cursor?.use {
                if (it.moveToFirst()) {
                    val index = it.getColumnIndex(OpenableColumns.DISPLAY_NAME)
                    if (index != -1) {
                        result = it.getString(index)
                    }
                }
            }
        }
        if (result == null) {
            result = uri.path
            val cut = result?.lastIndexOf('/')
            if (cut != null && cut != -1) {
                result = result?.substring(cut + 1)
            }
        }
        return result
    }

    private fun checkStoragePermission(): Boolean {
        return if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            ContextCompat.checkSelfPermission(
                this,
                Manifest.permission.READ_MEDIA_IMAGES
            ) == PackageManager.PERMISSION_GRANTED
        } else {
            ContextCompat.checkSelfPermission(
                this,
                Manifest.permission.READ_EXTERNAL_STORAGE
            ) == PackageManager.PERMISSION_GRANTED
        }
    }

    private fun requestStoragePermission() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            ActivityCompat.requestPermissions(
                this,
                arrayOf(Manifest.permission.READ_MEDIA_IMAGES),
                STORAGE_PERMISSION_CODE
            )
        } else {
            ActivityCompat.requestPermissions(
                this,
                arrayOf(Manifest.permission.READ_EXTERNAL_STORAGE),
                STORAGE_PERMISSION_CODE
            )
        }
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == STORAGE_PERMISSION_CODE) {
            if (grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                Toast.makeText(this, "Permissão concedida", Toast.LENGTH_SHORT).show()
            } else {
                Toast.makeText(this, "Permissão negada", Toast.LENGTH_SHORT).show()
            }
        }
    }
}