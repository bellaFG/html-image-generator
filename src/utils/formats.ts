export interface Formato {
  largura: number;
  altura: number;
}

export const FORMATOS: Record<string, Formato> = {
  feed: { largura: 1080, altura: 1080 },
  story: { largura: 1080, altura: 1920 },
  carrossel: { largura: 1080, altura: 1080 },
};

export const FORMATOS_DISPONIVEIS = Object.keys(FORMATOS);
