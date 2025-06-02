package com.example.sodcontrol.tellocontroller


import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.sodcontrol.R

class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_connect)

        val statusText = findViewById<TextView>(R.id.statusText)
        val connectButton = findViewById<Button>(R.id.btnConnect)
        val databaseButton = findViewById<Button>(R.id.btnDatabase)
        connectButton.setOnClickListener {
            Thread {
                try {
                    TelloCommandSender.sendCommand("command")
                    Thread.sleep(100)
                    TelloCommandSender.sendCommand("streamon")

                    runOnUiThread {
                        statusText.text = "Connected. Launching control screen..."
                        startActivity(Intent(this, ControlActivity::class.java))
                        finish()
                    }
                } catch (e: Exception) {
                    runOnUiThread {
                        Toast.makeText(this, "Failed to connect to Tello", Toast.LENGTH_LONG).show()
                        statusText.text = "Connection failed. Please try again."
                    }
                }
            }.start()
        }

        databaseButton.setOnClickListener {
            runOnUiThread {
                statusText.text = "Connected. Launching database screen..."
                startActivity(Intent(this, DatabaseSender::class.java))
                finish()
            }
        }
    }
}
