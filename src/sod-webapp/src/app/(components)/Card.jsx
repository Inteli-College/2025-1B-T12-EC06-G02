export default function Card({children}){
    return(
        <div className="w-3/4 bg-white/70 backdrop-blur-sm p-4 md:p-6 flex justify-center flex-col rounded items-center shadow-lg gap-10">
            {children}
        </div>
    )
}