import { supabase } from "../backend/lib/supabase";

export const formatDate = (dateString) => {
    if (!dateString) return "Data não disponível";

    const date = new Date(dateString);
    return date.toLocaleString("pt-BR", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

export const downloadReport = async (fileName) => {
    try {
      const { data, error } = await supabase.storage
        .from("relatorios")
        .download(fileName);

      if (error) throw error;

      const url = URL.createObjectURL(data);
      const link = document.createElement("a");
      link.href = url;
      link.download = fileName;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error("Erro ao fazer download:", err);
      alert("Erro ao fazer download do arquivo. Tente novamente.");
    }
  };