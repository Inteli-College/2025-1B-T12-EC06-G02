import Image from "next/image"
import Link from "next/link"

function LoginPage() {
  return (
    <main className="relative min-h-screen w-full">
      {/* Background Image with Filter */}
      <div className="absolute inset-0 -z-10">
        <div className="relative w-full h-full">
          <Image
            src="/cityscape-background.png"
            alt="Cityscape background"
            fill
            quality={100}
            priority
            className="object-cover brightness-90"
          />
        </div>
      </div>

      {/* Content Container */}
      <div className="relative min-h-screen w-full flex items-center justify-center p-4">
        {/* Semi-transparent Login Card */}
        <div className="w-full max-w-md bg-white/80 backdrop-blur-sm p-8 md:p-12 rounded shadow-lg">
          <h1 className="text-[#434343] text-4xl md:text-5xl font-medium mb-8 leading-tight">
            Sistema Óptico
            <br />
            de Deteção
          </h1>

          <form className="space-y-4">
            <div>
              <input
                type="email"
                placeholder="E-mail"
                className="w-full p-4 border border-gray-200 rounded focus:outline-none focus:ring-1 focus:ring-[#2d608d] text-gray-700 placeholder-gray-400"
                required
              />
            </div>

            <div>
              <input
                type="password"
                placeholder="Senha"
                className="w-full p-4 border border-gray-200 rounded focus:outline-none focus:ring-1 focus:ring-[#2d608d] text-gray-700 placeholder-gray-400"
                required
              />
            </div>

            <button
              type="submit"
              className="w-full p-4 bg-[#2d608d] text-white text-xl font-medium rounded hover:bg-[#245179] transition-colors"
            >
              Login
            </button>
          </form>

          <div className="mt-4 text-center">
            <Link href="/forgot-password" className="text-[#2d608d] hover:underline">
              Esqueci minha senha
            </Link>
          </div>

          <div className="my-6 border-t border-gray-300"></div>

          <div className="text-center">
            <Link
              href="/register"
              className="inline-block px-12 py-4 bg-[#00c939] text-white text-xl font-medium rounded hover:bg-[#00b033] transition-colors"
            >
              Criar conta
            </Link>
          </div>
        </div>
      </div>
    </main>
  )
}

export default LoginPage
