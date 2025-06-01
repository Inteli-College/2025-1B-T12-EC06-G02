package com.example.sodcontrol.tellocontroller

import java.net.DatagramPacket
import java.net.DatagramSocket
import java.net.InetAddress

object TelloCommandSender {
    private val telloIP = InetAddress.getByName("192.168.10.1")
    private const val telloPort = 8889
    private val socket = DatagramSocket()

    fun sendCommand(command: String) {
        val buf = command.toByteArray()
        val packet = DatagramPacket(buf, buf.size, telloIP, telloPort)
        socket.send(packet)
    }
}