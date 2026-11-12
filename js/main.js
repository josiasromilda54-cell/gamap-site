// GAMAP Construções — interações do site

// ---------- Ano no rodapé ----------
document.getElementById('ano').textContent = new Date().getFullYear();

// ---------- Menu mobile ----------
const hamburger = document.getElementById('hamburger');
const menu = document.getElementById('menu');

hamburger.addEventListener('click', () => {
  menu.classList.toggle('aberto');
  hamburger.classList.toggle('ativo');
});

// fecha o menu ao clicar em um link
menu.querySelectorAll('a').forEach(link =>
  link.addEventListener('click', () => {
    menu.classList.remove('aberto');
    hamburger.classList.remove('ativo');
  })
);

// ---------- Animações de revelação ----------
const observador = new IntersectionObserver(entradas => {
  entradas.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('visivel');
      observador.unobserve(e.target);
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll('.reveal').forEach(el => observador.observe(el));

// ---------- Filtros do portfólio ----------
const filtros = document.querySelectorAll('.filtro');
const obras = document.querySelectorAll('.obra');

filtros.forEach(botao => {
  botao.addEventListener('click', () => {
    filtros.forEach(f => f.classList.remove('ativo'));
    botao.classList.add('ativo');
    const cat = botao.dataset.filtro;

    obras.forEach(obra => {
      const mostrar = cat === 'todas' || obra.dataset.cat === cat;
      obra.style.display = mostrar ? '' : 'none';
      if (mostrar) {
        obra.classList.remove('visivel');
        requestAnimationFrame(() => requestAnimationFrame(() => obra.classList.add('visivel')));
      }
    });
  });
});

// ---------- Formulário -> WhatsApp ----------
document.getElementById('formOrcamento').addEventListener('submit', e => {
  e.preventDefault();

  const nome = document.getElementById('fNome').value.trim();
  const tel = document.getElementById('fTel').value.trim();
  const tipo = document.getElementById('fTipo').value;
  const local = document.getElementById('fLocal').value.trim();
  const msg = document.getElementById('fMsg').value.trim();

  const texto = [
    'Olá! Vim pelo site da GAMAP Construções e quero um orçamento.',
    '',
    `*Nome:* ${nome}`,
    tel ? `*Telefone:* ${tel}` : null,
    `*Serviço:* ${tipo}`,
    local ? `*Local da obra:* ${local}` : null,
    msg ? `*Detalhes:* ${msg}` : null
  ].filter(Boolean).join('\n');

  window.open(
    'https://wa.me/5512997901456?text=' + encodeURIComponent(texto),
    '_blank'
  );
});
