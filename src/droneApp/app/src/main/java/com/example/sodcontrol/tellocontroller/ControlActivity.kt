package com.example.sodcontrol.tellocontroller

import android.Manifest
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.view.SurfaceHolder
import android.view.SurfaceView
import android.widget.Button
import android.widget.TextView
import android.widget.Toast
import androidx.activity.result.ActivityResultLauncher
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import com.example.sodcontrol.R
import com.example.sodcontrol.ui.theme.JoystickView
import com.example.sodcontrol.utils.FileUtils
import java.util.concurrent.Executors
import java.util.concurrent.TimeUnit

class ControlActivity : AppCompatActivity() {

    private lateinit var videoReceiver: TelloVideoReceiver
    private lateinit var pickMediaLauncher: ActivityResultLauncher<String>

    private var leftX = 0f
    private var leftY = 0f
    private var rightX = 0f
    private var rightY = 0f
    private var selectedImageUri: Uri? = null

    private val STORAGE_PERMISSION_CODE = 101

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        pickMediaLauncher = registerForActivityResult(ActivityResultContracts.GetContent()) { uri: Uri? ->
            if (uri != null) {
                selectedImageUri = uri
                Toast.makeText(this, "Imagem selecionada!", Toast.LENGTH_SHORT).show()

                // Envia pro Supabase
                SupabaseClient.uploadImageAndInsertRecord(
                    context = this,
                    localFilePath = FileUtils.getPath(this, uri) ?: "",
                    fileName = "imagem_selecionada.jpg"
                )
                Toast.makeText(this, "Imagem enviada para o banco!", Toast.LENGTH_SHORT).show()
            } else {
                Toast.makeText(this, "Nenhuma imagem selecionada", Toast.LENGTH_SHORT).show()
            }
        }

        // Verifica e pede permissão ao iniciar
        if (!checkStoragePermission()) {
            requestStoragePermission()
        }

        val surfaceView = findViewById<SurfaceView>(R.id.videoSurface)
        val takeoffButton = findViewById<Button>(R.id.btnTakeoff)
        val powerButton = findViewById<Button>(R.id.btnPower)
        val photoButton = findViewById<Button>(R.id.btnPhoto)
        val databaseButton = findViewById<Button>(R.id.btnDatabase)
        val statusInfo = findViewById<TextView>(R.id.statusInfo)
        val leftJoystick = findViewById<JoystickView>(R.id.leftJoystick)
        val rightJoystick = findViewById<JoystickView>(R.id.rightJoystick)

        // Initialize video receiver
        val holder = surfaceView.holder
        holder.addCallback(object : SurfaceHolder.Callback {
            override fun surfaceCreated(holder: SurfaceHolder) {
                videoReceiver = TelloVideoReceiver(holder.surface)
                videoReceiver.start()

                Thread {
                    TelloCommandSender.sendCommand("command")
                    Thread.sleep(100)
                    TelloCommandSender.sendCommand("streamon")
                }.start()
            }

            override fun surfaceChanged(holder: SurfaceHolder, format: Int, width: Int, height: Int) {}
            override fun surfaceDestroyed(holder: SurfaceHolder) {
                videoReceiver.stop()
            }
        })

        // Buttons
        takeoffButton.setOnClickListener {
            Thread { TelloCommandSender.sendCommand("takeoff") }.start()
        }

        powerButton.setOnClickListener {
            Thread {
                sendRcControl(0, 0, 0, 0)
                Thread.sleep(100)
                TelloCommandSender.sendCommand("land")
            }.start()
        }

        photoButton.setOnClickListener {
            // TODO: Add image capture from frame if desired
        }

        databaseButton.setOnClickListener {
            Toast.makeText(this, "Imagem sendo enviada...", Toast.LENGTH_SHORT).show()
            if (checkStoragePermission()) {
                pickMediaLauncher.launch("image/*")
            } else {
                requestStoragePermission()
            }
        }

        // Joystick controls
        leftJoystick.setJoystickListener { x, y ->
            leftX = x * 100
            leftY = y * 100
        }

        rightJoystick.setJoystickListener { x, y ->
            rightX = x * 100
            rightY = y * 100
        }

        // Periodic control sending
        val scheduler = Executors.newSingleThreadScheduledExecutor()
        scheduler.scheduleAtFixedRate({
            val lr = mapInput(rightX)
            val fb = mapInput(-rightY)
            val ud = mapInput(-leftY)
            val yaw = mapInput(leftX)
            sendRcControl(lr, fb, ud, yaw)
        }, 0, 100, TimeUnit.MILLISECONDS)
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

    private fun mapInput(raw: Float): Int {
        return raw.coerceIn(-100f, 100f).toInt()
    }

    private fun sendRcControl(lr: Int, fb: Int, ud: Int, yaw: Int) {
        val command = "rc $lr $fb $ud $yaw"
        TelloCommandSender.sendCommand(command)
    }
}