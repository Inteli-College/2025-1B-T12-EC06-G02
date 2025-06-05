import IconeHist from "../../../public/hist-icon.png";
import { Button } from "./ui/button";
import {useRouter} from "next/navigation";

export default function Historico (){
    const router = useRouter()

    function handleClick(){
      router.push('/history')
    }
    return(
        <Button className="!h-auto !p-2 text-white !text-md !md:text-xl rounded hover:bg-[#00b033] transition-colors" onClick={handleClick}>
          <img src={IconeHist.src} className="h-6"></img>Histórico
        </Button>
    )
}