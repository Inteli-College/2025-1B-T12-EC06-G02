package com.example.sodcontrol.tellocontroller

import android.os.Bundle
import android.view.SurfaceHolder
import android.view.SurfaceView
import android.widget.Button
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import com.example.sodcontrol.R
import com.example.sodcontrol.ui.theme.JoystickView
import java.util.concurrent.Executors
import java.util.concurrent.TimeUnit

class ControlActivity : AppCompatActivity() {

    private lateinit var videoReceiver: TelloVideoReceiver

    private var leftX = 0f
    private var leftY = 0f
    private var rightX = 0f
    private var rightY = 0f

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val surfaceView = findViewById<SurfaceView>(R.id.videoSurface)
        val takeoffButton = findViewById<Button>(R.id.btnTakeoff)
        val powerButton = findViewById<Button>(R.id.btnPower)
        val photoButton = findViewById<Button>(R.id.btnPhoto)
        val statusInfo = findViewById<TextView>(R.id.statusInfo)
        val leftJoystick = findViewById<JoystickView>(R.id.leftJoystick)
        val rightJoystick = findViewById<JoystickView>(R.id.rightJoystick)

        // Initialize video receiver when surface is ready
        val holder = surfaceView.holder
        holder.addCallback(object : SurfaceHolder.Callback {
            override fun surfaceCreated(holder: SurfaceHolder) {
                videoReceiver = TelloVideoReceiver(holder.surface)
                videoReceiver.start()

                // Send command to Tello to enable video
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

    private fun mapInput(raw: Float): Int {
        return raw.coerceIn(-100f, 100f).toInt()
    }

    private fun sendRcControl(lr: Int, fb: Int, ud: Int, yaw: Int) {
        val command = "rc $lr $fb $ud $yaw"
        TelloCommandSender.sendCommand(command)
    }
}

