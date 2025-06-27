package com.example.sodcontrol.tellocontroller

import java.net.DatagramPacket
import java.net.DatagramSocket
import java.net.InetAddress
import java.net.SocketTimeoutException

object TelloCommandSender {
    private val telloIP = InetAddress.getByName("192.168.10.1")
    private const val telloPort = 8889
    private val socket = DatagramSocket().apply {
        soTimeout = 2000 // 2 second timeout for response
    }

    // Fire-and-forget command (takeoff, rc, etc.)
    fun sendCommand(command: String) {
        val buf = command.toByteArray()
        val packet = DatagramPacket(buf, buf.size, telloIP, telloPort)
        socket.send(packet)
    }

    // Command that expects a response (battery, wifi)
    fun sendCommandWithResponse(command: String): String? {
        val buf = command.toByteArray()
        val packet = DatagramPacket(buf, buf.size, telloIP, telloPort)
        socket.send(packet)

        return try {
            val responseBuf = ByteArray(1024)
            val responsePacket = DatagramPacket(responseBuf, responseBuf.size)
            socket.receive(responsePacket)
            String(responsePacket.data, 0, responsePacket.length).trim()
        } catch (e: SocketTimeoutException) {
            null
        } catch (e: Exception) {
            e.printStackTrace()
            null
        }
    }
}
