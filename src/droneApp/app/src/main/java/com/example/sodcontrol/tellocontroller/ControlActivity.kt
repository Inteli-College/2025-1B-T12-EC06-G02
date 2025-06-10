package com.example.sodcontrol.tellocontroller

import android.annotation.SuppressLint
import android.content.Intent
import android.graphics.Bitmap
import android.graphics.SurfaceTexture
import android.media.MediaScannerConnection
import android.os.Bundle
import android.os.Environment
import android.view.Surface
import android.view.TextureView
import android.widget.Button
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.sodcontrol.R
import com.example.sodcontrol.ui.theme.JoystickView
import java.io.File
import java.io.FileOutputStream
import java.text.SimpleDateFormat
import java.util.*
import java.util.concurrent.Executors
import java.util.concurrent.TimeUnit

class ControlActivity : AppCompatActivity() {

    private lateinit var videoReceiver: TelloVideoReceiver
    private lateinit var textureView: TextureView

    private var leftX = 0f
    private var leftY = 0f
    private var rightX = 0f
    private var rightY = 0f

    @SuppressLint("DiscouragedApi")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        textureView = findViewById(R.id.videoSurface)
        val takeoffButton = findViewById<Button>(R.id.btnTakeoff)
        val powerButton = findViewById<Button>(R.id.btnPower)
        val photoButton = findViewById<Button>(R.id.btnPhoto)
        val disconnectButton = findViewById<Button>(R.id.btnDisconnect)
        val statusInfo = findViewById<TextView>(R.id.statusInfo)
        val leftJoystick = findViewById<JoystickView>(R.id.leftJoystick)
        val rightJoystick = findViewById<JoystickView>(R.id.rightJoystick)

        textureView.surfaceTextureListener = object : TextureView.SurfaceTextureListener {
            override fun onSurfaceTextureAvailable(surfaceTexture: SurfaceTexture, width: Int, height: Int) {
                val surface = Surface(surfaceTexture)
                videoReceiver = TelloVideoReceiver(surface)
                videoReceiver.start()

                Thread {
                    TelloCommandSender.sendCommand("command")
                    Thread.sleep(100)
                    TelloCommandSender.sendCommand("streamon")
                }.start()
            }

            override fun onSurfaceTextureSizeChanged(surface: SurfaceTexture, width: Int, height: Int) {}
            override fun onSurfaceTextureDestroyed(surface: SurfaceTexture): Boolean {
                videoReceiver.stop()
                return true
            }

            override fun onSurfaceTextureUpdated(surface: SurfaceTexture) {}
        }

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

        disconnectButton.setOnClickListener {
            Thread {
                sendRcControl(0, 0, 0, 0)
                Thread.sleep(200)
                TelloCommandSender.sendCommand("land")
                videoReceiver.stop()
                runOnUiThread {
                    val intent = Intent(this, MainActivity::class.java)
                    intent.flags = Intent.FLAG_ACTIVITY_CLEAR_TOP or Intent.FLAG_ACTIVITY_NEW_TASK
                    startActivity(intent)
                    finish()
                }
            }.start()
        }

        photoButton.setOnClickListener {
            val bitmap = textureView.bitmap
            if (bitmap != null) {
                saveBitmapToGallery(bitmap)
            } else {
                Toast.makeText(this, "Failed to capture frame", Toast.LENGTH_SHORT).show()
            }
        }

        leftJoystick.setJoystickListener { x, y ->
            leftX = x * 100
            leftY = y * 100
        }

        rightJoystick.setJoystickListener { x, y ->
            rightX = x * 100
            rightY = y * 100
        }

        val scheduler = Executors.newSingleThreadScheduledExecutor()
        scheduler.scheduleAtFixedRate({
            val lr = mapInput(rightX)
            val fb = mapInput(-rightY)
            val ud = mapInput(-leftY)
            val yaw = mapInput(leftX)
            sendRcControl(lr, fb, ud, yaw)
        }, 0, 100, TimeUnit.MILLISECONDS)

        val batteryAndWifiScheduler = Executors.newSingleThreadScheduledExecutor()

        batteryAndWifiScheduler.scheduleAtFixedRate({
            val battery = TelloCommandSender.sendCommandWithResponse("battery?")
            val wifi = TelloCommandSender.sendCommandWithResponse("wifi?")

            runOnUiThread {
                statusInfo.text = "Battery: ${battery ?: "?"}%  |  Wi-Fi: ${wifi ?: "?"} SNR"
            }
        }, 0, 5, TimeUnit.SECONDS)
    }

    private fun saveBitmapToGallery(bitmap: Bitmap) {
        val contentValues = android.content.ContentValues().apply {
            val timestamp = SimpleDateFormat("yyyyMMdd_HHmmss", Locale.getDefault()).format(Date())
            put(android.provider.MediaStore.Images.Media.DISPLAY_NAME, "Tello_$timestamp.jpg")
            put(android.provider.MediaStore.Images.Media.MIME_TYPE, "image/jpeg")
            put(android.provider.MediaStore.Images.Media.RELATIVE_PATH, "Pictures/SOD")
            put(android.provider.MediaStore.Images.Media.IS_PENDING, 1)
        }

        val contentResolver = contentResolver
        val uri = contentResolver.insert(android.provider.MediaStore.Images.Media.EXTERNAL_CONTENT_URI, contentValues)

        uri?.let {
            try {
                contentResolver.openOutputStream(uri)?.use { out ->
                    bitmap.compress(Bitmap.CompressFormat.JPEG, 100, out)
                }

                contentValues.clear()
                contentValues.put(android.provider.MediaStore.Images.Media.IS_PENDING, 0)
                contentResolver.update(uri, contentValues, null, null)

                runOnUiThread {
                    Toast.makeText(this, "Photo saved to gallery in SOD", Toast.LENGTH_SHORT).show()
                }

            } catch (e: Exception) {
                e.printStackTrace()
                runOnUiThread {
                    Toast.makeText(this, "Failed to save photo", Toast.LENGTH_SHORT).show()
                }
            }
        } ?: runOnUiThread {
            Toast.makeText(this, "Could not create MediaStore entry", Toast.LENGTH_SHORT).show()
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
