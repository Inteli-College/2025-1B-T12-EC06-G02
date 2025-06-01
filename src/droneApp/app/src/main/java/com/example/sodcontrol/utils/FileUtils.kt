package com.example.sodcontrol.utils

import android.content.Context
import android.database.Cursor
import android.net.Uri
import android.provider.OpenableColumns
import java.io.File
import java.io.FileOutputStream
import java.io.InputStream
import java.io.OutputStream

object FileUtils {

    fun getPath(context: Context, uri: Uri): String? {
        val fileName = getFileName(context, uri) ?: return null
        val file = File(context.cacheDir, fileName)
        try {
            val inputStream: InputStream? = context.contentResolver.openInputStream(uri)
            val outputStream: OutputStream = FileOutputStream(file)
            inputStream?.copyTo(outputStream)
            inputStream?.close()
            outputStream.close()
        } catch (e: Exception) {
            e.printStackTrace()
            return null
        }
        return file.absolutePath
    }

    private fun getFileName(context: Context, uri: Uri): String? {
        var result: String? = null
        if (uri.scheme == "content") {
            val cursor: Cursor? = context.contentResolver.query(
                uri, null, null, null, null
            )
            try {
                cursor?.let {
                    if (it.moveToFirst()) {
                        result =
                            it.getString(it.getColumnIndexOrThrow(OpenableColumns.DISPLAY_NAME))
                    }
                }
            } finally {
                cursor?.close()
            }
        }
        if (result == null) {
            result = uri.path
            val cut = result?.lastIndexOf('/') ?: -1
            if (cut != -1) {
                result = result?.substring(cut + 1)
            }
        }
        return result
    }
}