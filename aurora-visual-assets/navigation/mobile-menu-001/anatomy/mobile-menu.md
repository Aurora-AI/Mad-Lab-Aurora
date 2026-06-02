# Anatomy: Mobile Menu (navigation-mobile-menu-001)

## Architecture
O `Mobile Menu` é um componente de navegação em tela cheia (overlay) projetado para densidade mobile. Ele utiliza um sistema de **Staggered Spring Entry**, onde os itens da lista entram sequencialmente com física de mola.

## Core Components
- **MobileMenu**: O ponto de entrada que gerencia os estados de overlay e backdrop.
- **AnimatePresence**: Utilizado para garantir que as animações de saída (exit) ocorram suavemente ao fechar o menu.

## Techniques & Patterns
- **P042: Spring-Loaded Entry**: Uso de `type: "spring"` com `damping: 30` para eliminar o "feeling" linear de templates comuns.
- **P043: Backdrop Blur Compositing**: O uso de `backdrop-blur-sm` combinado com `bg-black/80` cria profundidade sem sacrificar o contraste da tipografia.
- **P044: Hidden-to-Visible Transition**: Itens de menu movem-se de `x: 20` para `x: 0` enquanto a opacidade sobe, criando uma sensação de "deslize editorial".

## Dependency Analysis
- **Framer Motion**: Requisito central para orquestração de molas e AnimatePresence.
- **Lucide React**: Ícones de navegação.

## Performance
- **Isolation**: O menu opera em um portal z-index isolado (`z-[200]`) para evitar conflitos de renderização com seções imersivas (Three.js) da página inferior.
