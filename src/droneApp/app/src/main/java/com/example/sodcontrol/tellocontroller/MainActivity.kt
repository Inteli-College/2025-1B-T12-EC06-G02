package com.example.sodcontrol.tellocontroller

import android.os.Bundle
import android.widget.Button
import android.widget.VideoView
import androidx.appcompat.app.AppCompatActivity
import com.example.sodcontrol.R
import java.lang.Thread.sleep

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val videoView = findViewById<VideoView>(R.id.videoView)
        val takeoffButton = findViewById<Button>(R.id.btnTakeoff)
        val landButton = findViewById<Button>(R.id.btnLand)
        val photoButton = findViewById<Button>(R.id.btnPhoto)

        // Initialize Tello UDP connection
        Thread {
            TelloCommandSender.sendCommand("command")
            sleep(100)
            TelloCommandSender.sendCommand("streamon")
        }.start()

        videoView.setVideoPath("udp://@0.0.0.0:11111")
        videoView.start()

        takeoffButton.setOnClickListener {
            Thread { TelloCommandSender.sendCommand("takeoff") }.start()
        }

        landButton.setOnClickListener {
            Thread { TelloCommandSender.sendCommand("land") }.start()
        }

        photoButton.setOnClickListener {
            // TODO: sistema de tirar foto.
        }
    }
}