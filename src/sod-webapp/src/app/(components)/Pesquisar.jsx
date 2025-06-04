import { InputBase, IconButton, TextField } from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import { DatePicker, LocalizationProvider } from "@mui/x-date-pickers";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { useState } from "react";

export default function Pesquisar({ data, handleRelatorio, handleData }) {
  const [relatorioPesquisado, setRelatorioPesquisado] = useState("");

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <div className="flex justify-evenly">
        <div id="nome" className="flex items-center">
          <TextField
            label="Pesquisar relatório"
            variant="standard"
            onChange={(event) => setRelatorioPesquisado(event.target.value)}
          />
          <IconButton
            type="button"
            aria-label="search"
            onClick={() => handleRelatorio(relatorioPesquisado)}
          >
            <SearchIcon />
          </IconButton>
        </div>
        <div id="data">
          <DatePicker
            label="Filtrar por Data"
            format="DD/MM/YYYY"
            value={data || null}
            onChange={(newDate) => handleData(newDate)}
            slotProps={{ textField: { variant: "standard", size: "small" } }}
          />
        </div>
      </div>
    </LocalizationProvider>
  );
}
