import java.util.Properties
import java.io.FileInputStream

plugins {
    id("com.android.application")
    // The Flutter Gradle Plugin must be applied after the Android and Kotlin Gradle plugins.
    id("dev.flutter.flutter-gradle-plugin")
}

// Firma de publicación: android/key.properties (ignorado por git; la llave vive en
// ~/.config/onelingo-firma). Sin ese archivo, release se firma con la llave de depuración.
val firmaPropiedades = Properties().apply {
    val archivo = rootProject.file("key.properties")
    if (archivo.exists()) load(FileInputStream(archivo))
}

android {
    namespace = "com.torisoftt.onelingo"
    compileSdk = flutter.compileSdkVersion
    ndkVersion = flutter.ndkVersion

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    defaultConfig {
        // TODO: Specify your own unique Application ID (https://developer.android.com/studio/build/application-id.html).
        applicationId = "com.torisoftt.onelingo"
        // You can update the following values to match your application needs.
        // For more information, see: https://flutter.dev/to/review-gradle-config.
        minSdk = flutter.minSdkVersion
        targetSdk = flutter.targetSdkVersion
        // Uses the version code from pubspec.yaml. When using split APKs, 1000 * ABI_VERSION
        // is added automatically by Flutter. (https://developer.android.com/studio/build/configure-apk-splits#configure-APK-versions)
        // You can force using the value of versionCode by specifying the `-P force-version-code-ignoring-abi=true`
        // flag during build.
        versionCode = flutter.versionCode
        versionName = flutter.versionName
    }

    signingConfigs {
        if (firmaPropiedades.containsKey("storeFile")) {
            create("publicacion") {
                storeFile = file(firmaPropiedades.getProperty("storeFile"))
                storePassword = firmaPropiedades.getProperty("storePassword")
                keyAlias = firmaPropiedades.getProperty("keyAlias")
                keyPassword = firmaPropiedades.getProperty("keyPassword")
            }
        }
    }

    buildTypes {
        release {
            signingConfig = if (firmaPropiedades.containsKey("storeFile")) signingConfigs.getByName("publicacion")
                else signingConfigs.getByName("debug")
        }
    }
}

kotlin {
    compilerOptions {
        jvmTarget = org.jetbrains.kotlin.gradle.dsl.JvmTarget.JVM_17
    }
}

flutter {
    source = "../.."
}
