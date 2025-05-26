import Card from "./Card"
import Usuario from "./Usuario"
import MiniGaleria from "./miniGaleria"

export default function Uploads({images, name, selection}){
    return(
        <Card>
            {/*só testando o github, lembrar de implementar o upload via servidor... */}
            <Usuario nome={name}/>
            <MiniGaleria images={images}/>
        </Card>
    )
}