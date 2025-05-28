package com.example.sodcontrol.tellocontroller

import android.content.Context
import android.widget.Toast
import io.ktor.client.*
import io.ktor.client.call.*
import io.ktor.client.engine.android.*
import io.ktor.client.plugins.contentnegotiation.*
import io.ktor.client.request.*
import io.ktor.client.statement.*
import io.ktor.http.*
import io.ktor.serialization.kotlinx.json.*
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import java.io.File
import com.example.sodcontrol.BuildConfig


@OptIn(kotlinx.serialization.InternalSerializationApi::class)
object SupabaseClient {

    private const val BASE_URL = BuildConfig.BASE_URL
    private const val API_KEY = BuildConfig.SUPABASE_API_KEY
    private const val BEARER_TOKEN = BuildConfig.SUPABASE_BEARER_TOKEN

    private val client = HttpClient(Android) {
        install(ContentNegotiation) {
            json(Json { ignoreUnknownKeys = true })
        }
    }

    @Serializable
    data class ImageData(
        val file_path: String,
        val file_name: String,
        val type: String,
        val size_kb: Int,
        val app: Boolean
    )


    fun uploadImageAndInsertRecord(context: Context, localFilePath: String, fileName: String) {
        CoroutineScope(Dispatchers.IO).launch {
            try {
                val file = File(localFilePath)
                if (!file.exists()) {
                    throw IllegalArgumentException("Arquivo não encontrado: $localFilePath")
                }

                val mimeType = when {
                    fileName.endsWith(".png", ignoreCase = true) -> "image/png"
                    fileName.endsWith(".jpg", ignoreCase = true) || fileName.endsWith(".jpeg", ignoreCase = true) -> "image/jpeg"
                    else -> "application/octet-stream"
                }

                val sizeKb = (file.length() / 1024).toInt()
                val filePathInBucket = "imagens/$fileName"

                // Upload para o bucket
                val uploadResponse: HttpResponse = client.put("$BASE_URL/storage/v1/object/$filePathInBucket") {
                    headers {
                        append("apikey", API_KEY)
                        append("Authorization", "Bearer $BEARER_TOKEN")
                        append(HttpHeaders.ContentType, mimeType)
                    }
                    setBody(file.readBytes())
                }

                if (uploadResponse.status.isSuccess()) {
                    // Registro na tabela 'images'
                    val imageData = ImageData(
                        file_path = filePathInBucket,
                        file_name = fileName,
                        type = mimeType,
                        size_kb = sizeKb,
                        app = true
                    )

                    val insertResponse: String = client.post("$BASE_URL/rest/v1/images") {
                        contentType(ContentType.Application.Json)
                        headers {
                            append("apikey", API_KEY)
                            append("Authorization", "Bearer $BEARER_TOKEN")
                            append("Prefer", "return=representation")
                        }
                        setBody(listOf(imageData))
                    }.body()

                    CoroutineScope(Dispatchers.Main).launch {
                        Toast.makeText(context, "Upload e registro OK! $insertResponse", Toast.LENGTH_SHORT).show()
                    }
                } else {
                    throw Exception("Falha no upload: ${uploadResponse.status}")
                }
            } catch (e: Exception) {
                e.printStackTrace()
                CoroutineScope(Dispatchers.Main).launch {
                    Toast.makeText(context, "Erro: ${e.message}", Toast.LENGTH_LONG).show()
                }
            }
        }
    }
}
