const DISABLED_MESSAGE =
  "O assistente foi desativado neste frontend para evitar exposição de segredos. A reativação exige um endpoint backend protegido pelo AuroraVault.";

export function isAssistantConfigured() {
  return false;
}

export async function askAssistant(_prompt: string) {
  return DISABLED_MESSAGE;
}
