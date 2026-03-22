import { z } from "zod";
import { carregarBrand } from "../templates/template-manager.js";

export const verMarcaDefinicao = {
  name: "ver_marca",
  description:
    "Consulta a identidade visual da empresa — cores, fontes, logo e estilos padrão. Use antes de gerar posts para manter a coerência visual da marca.",
  schema: {},
};

export const verMarcaSchema = z.object({});

export async function verMarcaHandler() {
  const brand = carregarBrand();
  return {
    content: [
      {
        type: "text" as const,
        text: JSON.stringify(brand, null, 2),
      },
    ],
  };
}
