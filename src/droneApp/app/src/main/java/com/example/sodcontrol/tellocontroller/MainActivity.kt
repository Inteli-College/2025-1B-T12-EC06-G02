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
                        statusText.text = "Conectado, iniciando controle..."
                        startActivity(Intent(this, ControlActivity::class.java))
                        finish()
                    }
                } catch (e: Exception) {
                    runOnUiThread {
                        Toast.makeText(this, "Failed to connect to Tello", Toast.LENGTH_LONG).show()
                        statusText.text = "Falha de conexão, cheque conexão Wi-Fi com o Drone."
                    }
                }
            }.start()
        }

        databaseButton.setOnClickListener {
            runOnUiThread {
                statusText.text = "Iniciando..."
                startActivity(Intent(this, DatabaseSender::class.java))
                finish()
            }
        }
    }
}
