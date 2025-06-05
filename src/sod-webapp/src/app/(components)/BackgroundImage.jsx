import Image from "next/image";

export default function BackgroundImage({ children }) {
  return (
    <div className="relative w-full min-h-screen">
      {/* Background Image */}
      <div className="absolute inset-0 -z-10">
        <Image
          src="/cityscape-background.png"
          alt="City Background"
          fill
          quality={100}
          priority
          className="object-cover brightness-90"
        />
      </div>

      {/* Content */}
      <div className="relative z-10 flex items-center justify-center h-full">
        <div className="relative min-h-screen w-full flex flex-col md:flex-row gap-5 md:gap-0 items-center justify-center p-4">
            {children}
          </div>
      </div>
    </div>
  );
}
