import Card from "./Card"
import Usuario from "./Usuario"
import MiniGaleria from "./miniGaleria"

export default function Uploads({images, name, selection}){
    return(
        <Card>
            <Usuario nome={name}/>
            <MiniGaleria images={images}/>
        </Card>
    )
}