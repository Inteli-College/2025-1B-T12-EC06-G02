export default function Card({children}){
    return(
        <div className="md:w-3/4 min-w-[75%] bg-white/70 backdrop-blur-sm p-6 flex justify-center flex-col rounded items-center shadow-lg gap-5 md:gap-10">
            {children}
        </div>
    )
}