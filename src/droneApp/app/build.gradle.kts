import org.jetbrains.kotlin.gradle.dsl.JvmTarget
import java.util.Properties
import java.io.FileInputStream

val props = Properties()
val localPropertiesFile = rootProject.file("local.properties")
if (localPropertiesFile.exists()) {
    props.load(FileInputStream(localPropertiesFile))
}

plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    id("org.jetbrains.kotlin.plugin.compose")
    id("org.jetbrains.kotlin.plugin.serialization") version "2.0.21"
}

android {
    namespace = "com.example.sodcontrol"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.example.sodcontrol"
        minSdk = 24
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"

        buildConfigField("String", "SUPABASE_API_KEY", "\"${props.getProperty("SUPABASE_API_KEY")}\"")
        buildConfigField("String", "SUPABASE_BEARER_TOKEN", "\"${props.getProperty("SUPABASE_BEARER_TOKEN")}\"")
        buildConfigField("String", "BASE_URL", "\"${props.getProperty("BASE_URL")}\"")
    }

    buildFeatures {
        compose = false
        buildConfig = true
    }
}

dependencies {
    val composeBom = platform("androidx.compose:compose-bom:2023.10.01")
    implementation(composeBom)
    androidTestImplementation(composeBom)

    implementation(libs.activity.compose)
    implementation(libs.ui)
    implementation(libs.material3)
    implementation(libs.ui.tooling.preview)
    implementation(libs.androidx.appcompat)
    implementation(libs.libvlc.core)
    debugImplementation(libs.ui.tooling)
    debugImplementation(libs.ui.test.manifest)

    implementation(libs.androidx.lifecycle.runtime.ktx.v262)
    implementation(libs.androidx.core.ktx.v1120)

    // Ktor Client compatível com Kotlin 2.0.21
    implementation("io.ktor:ktor-client-android:2.3.9")
    implementation("io.ktor:ktor-client-content-negotiation:2.3.9")
    implementation("io.ktor:ktor-serialization-kotlinx-json:2.3.9")
    implementation("io.ktor:ktor-client-core:2.3.9")
    implementation("io.ktor:ktor-client-okhttp:2.3.9")
    implementation("io.github.cdimascio:dotenv-kotlin:6.4.1")


}

tasks.withType<org.jetbrains.kotlin.gradle.tasks.KotlinCompile>().configureEach {
    compilerOptions {
        jvmTarget.set(JvmTarget.JVM_1_8)
    }
}