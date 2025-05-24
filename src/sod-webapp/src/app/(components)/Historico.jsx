import IconeHist from "../../../public/hist-icon.png";
import { Button } from "./ui/button";


export default function Historico (){
    return(
        <Button className="!h-auto w-1/6 !p-2 text-white !text-xl rounded hover:bg-[#00b033] transition-colors">
          <img src={IconeHist.src} className="h-6"></img>Histórico
        </Button>
    )
}