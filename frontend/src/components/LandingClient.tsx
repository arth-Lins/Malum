'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';

const title = 'Malum';
const phrase = 'Todo processo esconde o que sobra. A Malum encontra.';

function TypeHero() {
  const [heading, setHeading] = useState('');
  const [support, setSupport] = useState('');
  const [reducedMotion, setReducedMotion] = useState(false);
  useEffect(() => {
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    setReducedMotion(reduced);
    if (reduced) { setHeading(title); setSupport(phrase); return; }
    let index = 0;
    const titleTimer = window.setInterval(() => {
      index += 1; setHeading(title.slice(0, index));
      if (index !== title.length) return;
      window.clearInterval(titleTimer);
      let phraseIndex = 0;
      const phraseTimer = window.setInterval(() => { phraseIndex += 1; setSupport(phrase.slice(0, phraseIndex)); if (phraseIndex === phrase.length) window.clearInterval(phraseTimer); }, 26);
    }, 105);
    return () => window.clearInterval(titleTimer);
  }, []);
  const typing = !reducedMotion && (heading.length < title.length || support.length < phrase.length);
  return <><h1 className="hero-title">{heading}<span className={typing ? 'cursor' : 'cursor done'} aria-hidden="true">_</span></h1><p className="hero-phrase">{support}</p></>;
}

export default function LandingClient() {
  return <main><nav className="nav"><Link className="logo" href="/">M</Link><div><a href="#introducao">INTRODUÇÃO</a><a href="#quem-somos">QUEM SOMOS</a><Link href="/entrar">ENTRAR</Link></div></nav><section className="hero hero-full grid-bg"><div className="hero-orbit orbit-one" aria-hidden="true"/><div className="hero-orbit orbit-two" aria-hidden="true"/><div className="hero-apple apple-one" aria-hidden="true">●</div><div className="hero-apple apple-two" aria-hidden="true">●</div><span className="tag">// inteligência para quem produz</span><TypeHero/><p className="hero-sub">Envie suas planilhas e descubra onde materiais, energia e dinheiro estão sendo perdidos — e como parar.</p><div className="actions"><Link className="button utility-action" href="/precos">Use agora <span>↗</span></Link><Link className="button ghost" href="/entrar">Entrar <span>↗</span></Link></div><div className="hero-chart hero-chart-bars" aria-hidden="true"><i/><i/><i/><i/></div><p className="hero-scroll">ROLE PARA DESCOBRIR ↓</p></section><section id="introducao" className="light-section"><span className="eyebrow">01 / INTRODUÇÃO</span><h2>Desperdício não mora no total.<br/>Mora nos detalhes.</h2><p className="lead">A Malum lê suas planilhas de consumo, compara recursos usados com volume produzido e mostra onde há perda de matéria-prima, uso ineficiente de água ou energia e padrões fora do normal.</p><div className="steps"><article><b>01</b><h3>Envie</h3><p>Sua planilha comum, sem integração difícil.</p></article><article><b>02</b><h3>Pergunte</h3><p>Diga o que importa para seu processo.</p></article><article><b>03</b><h3>Entenda</h3><p>Dados, contexto e ações priorizadas.</p></article></div><p className="where"><strong>Onde?</strong> Nas etapas que consomem mais do que deveriam. <strong>Como?</strong> Comparando consumo, volume produzido e indicadores de eficiência.</p><Link className="button dark utility-action" href="/precos">Ver assinaturas <span>↗</span></Link></section><section id="quem-somos" className="about"><span className="eyebrow">02 / QUEM SOMOS</span><h2>AdaCore,<br/><em>possibilidade aplicada.</em></h2><p>A AdaCore é um núcleo de inovação que usa tecnologia para resolver problemas reais de produção. Nosso nome homenageia Ada Lovelace, pioneira que enxergou nas máquinas mais do que cálculo: enxergou possibilidade. Unimos estatística, inteligência artificial e design para tornar a eficiência acessível em qualquer escala.</p><ul className="team"><li><strong>Arthur Enrique Rodrigues Lins</strong><span>Coordenação do projeto</span></li><li><strong>Maria Lauria de Abreu Barbosa Rodrigues Freitas</strong><span>Programação chefe</span></li><li><strong>Maria Isabella Vieira Silva</strong><span>Redação de textos</span></li><li><strong>Isabella Antonelle da Costa Sousa Martins</strong><span>Design UX/UI</span></li><li><strong>Prof. Hélio de Sousa Campos Filho</strong><span>Professor orientador</span></li></ul></section><footer>Malum © 2026 <span>produção sustentável, sem adivinhação.</span></footer></main>;
}
