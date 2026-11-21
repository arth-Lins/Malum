import Link from 'next/link';

const plans = [['Semente', 'R$ 0', '3 análises / mês', 'Até 1.000 linhas', 'Chat limitado'], ['Oficina', 'R$ 39', '30 análises / mês', 'Até 10.000 linhas', 'Chat ampliado'], ['Fábrica', 'R$ 119', '150 análises / mês', 'Até 100.000 linhas', 'Chat amplo + relatório'], ['Núcleo', 'Sob consulta', 'Uso personalizado', 'Tamanho personalizado', 'Para equipes']];

export default function Precos() {
  return <main className="pricing"><nav className="nav"><Link className="logo" href="/">M</Link><Link href="/">Voltar ao início</Link></nav><header><span className="tag">// ASSINATURAS</span><h1>Escolha seu ritmo.<br /><em>Crie a conta depois.</em></h1><p>Valores de demonstração. Você só informa seus dados depois de escolher um plano.</p></header><section className="plans">{plans.map((plan, index) => <article className={'plan ' + (index === 2 ? 'featured' : '')} key={plan[0]}>{index === 2 && <b className="recommend">RECOMENDADO</b>}<h2>{plan[0]}</h2><strong>{plan[1]}<small>{index < 3 && ' / mês'}</small></strong><ul>{plan.slice(2).map(item => <li key={item}>✓ {item}</li>)}</ul><Link className={'button utility-action ' + (index === 2 ? 'dark' : '')} href="/cadastro">Usar {plan[0]} <span>↗</span></Link></article>)}</section><Link className="skip" href="/cadastro">Começar com o plano gratuito →</Link></main>;
}
