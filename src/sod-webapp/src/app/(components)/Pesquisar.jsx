import { IconButton, TextField } from "@mui/material";
import ClearIcon from "@mui/icons-material/Clear";
import SearchIcon from "@mui/icons-material/Search";
import { DatePicker, LocalizationProvider } from "@mui/x-date-pickers";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { useState } from "react";
import dayjs from "dayjs";

export default function Pesquisar({ data, handleRelatorio, handleData }) {
  const [relatorioPesquisado, setRelatorioPesquisado] = useState("");

  function handleChange(newDate) {
    if (newDate === null) {
      handleData(null); // limpa a data
      return;
    }

    const selectedDate = dayjs(newDate);
    if (
      selectedDate.isValid() &&
      selectedDate.isBefore(dayjs().add(1, "day"))
    ) {
      handleData(newDate);
    }
  }

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <div className="flex justify-evenly">
        <div id="nome" className="flex items-center">
          <TextField
            label="Insira o nº do relatório"
            type="number"
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
        <div id="data" className="flex items-center gap-1">
          <DatePicker
            label="Filtrar por Data"
            format="DD/MM/YYYY"
            value={data || null}
            onChange={handleChange}
            minDate={dayjs("1990-01-01")}
            maxDate={dayjs()}
            slotProps={{
              textField: { variant: "standard", size: "small" },
            }}
          />
          {data && <IconButton
            onClick={() => handleData(null)}
            aria-label="Limpar data"
            title="Limpar data"
          >
            <ClearIcon />
          </IconButton>}
        </div>
      </div>
    </LocalizationProvider>
  );
}
