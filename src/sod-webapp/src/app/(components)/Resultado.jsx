export default function Resultado({valor, label}) {
    return(
        <div className="flex flex-col justify-center items-center text-center">
            <h2 className="text-2xl md:text-5xl">{valor}</h2>
            <p className="text-lg md:text-3xl">{label}</p>
        </div>
    )
}