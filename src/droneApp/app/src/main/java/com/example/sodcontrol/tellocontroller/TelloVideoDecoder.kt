package com.example.sodcontrol.tellocontroller

import android.media.MediaCodec
import android.media.MediaFormat
import android.view.Surface
import java.net.DatagramPacket
import java.net.DatagramSocket
import java.nio.ByteBuffer
import java.util.concurrent.atomic.AtomicBoolean

class TelloVideoReceiver(private val surface: Surface) {

    private val decoder: MediaCodec = MediaCodec.createDecoderByType("video/avc")
    private val running = AtomicBoolean(false)
    private val socket = DatagramSocket(11111)

    private var nalBuffer = ByteArray(0)
    private var sps: ByteArray? = null
    private var pps: ByteArray? = null
    private var decoderConfigured = false
    private var corruptedFrames = 0

    fun start() {
        running.set(true)
        Thread {
            val buffer = ByteArray(2048)
            val packet = DatagramPacket(buffer, buffer.size)

            while (running.get()) {
                try {
                    socket.receive(packet)
                    val data = packet.data.copyOf(packet.length)
                    nalBuffer += data

                    while (true) {
                        val nalStart = findNalStart(nalBuffer)
                        val nextStart = findNalStart(nalBuffer, nalStart + 4)

                        if (nalStart < 0 || nextStart < 0) break

                        val nal = nalBuffer.copyOfRange(nalStart, nextStart)
                        nalBuffer = nalBuffer.copyOfRange(nextStart, nalBuffer.size)
                        handleNAL(nal)
                    }
                } catch (e: Exception) {
                    e.printStackTrace()
                }
            }
        }.start()
    }

    private fun findNalStart(data: ByteArray, offset: Int = 0): Int {
        for (i in offset until data.size - 4) {
            if (data[i] == 0.toByte() && data[i + 1] == 0.toByte() && data[i + 2] == 0.toByte() && data[i + 3] == 1.toByte()) {
                return i
            }
        }
        return -1
    }

    private fun handleNAL(nal: ByteArray) {
        if (nal.size < 5) return
        val nalType = nal[4].toInt() and 0x1F

        when (nalType) {
            7 -> sps = nal
            8 -> pps = nal
            5 -> { // I-frame
                if (!decoderConfigured && sps != null && pps != null) {
                    configureDecoder()
                }
                if (decoderConfigured) {
                    sps?.let { decode(it) }
                    pps?.let { decode(it) }
                    decode(nal)
                }
            }
            else -> {
                if (decoderConfigured) {
                    decode(nal)
                }
            }
        }
    }

    private fun configureDecoder() {
        val format = MediaFormat.createVideoFormat("video/avc", 960, 720)
        sps?.let { format.setByteBuffer("csd-0", ByteBuffer.wrap(it)) }
        pps?.let { format.setByteBuffer("csd-1", ByteBuffer.wrap(it)) }

        decoder.configure(format, surface, null, 0)
        decoder.start()
        decoderConfigured = true
    }

    private fun decode(nal: ByteArray) {
        if (nal.size < 100) return // Discard suspiciously small NALs

        val inputIndex = decoder.dequeueInputBuffer(10_000)
        if (inputIndex >= 0) {
            val inputBuffer = decoder.getInputBuffer(inputIndex)
            inputBuffer?.clear()
            inputBuffer?.put(nal)
            decoder.queueInputBuffer(inputIndex, 0, nal.size, System.nanoTime() / 1000, 0)
        } else {
            corruptedFrames++
        }

        val bufferInfo = MediaCodec.BufferInfo()
        var outputIndex = decoder.dequeueOutputBuffer(bufferInfo, 0)
        while (outputIndex >= 0) {
            decoder.releaseOutputBuffer(outputIndex, true)
            outputIndex = decoder.dequeueOutputBuffer(bufferInfo, 0)
        }

        // Attempt recovery on persistent corruption
        if (corruptedFrames > 10) {
            try {
                decoder.stop()
                decoderConfigured = false
                configureDecoder()
                corruptedFrames = 0
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }

    fun stop() {
        running.set(false)
        decoder.stop()
        decoder.release()
        socket.close()
    }
}
