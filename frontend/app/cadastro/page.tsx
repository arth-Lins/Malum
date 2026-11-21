'use client';

import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useState } from 'react';
import { AuthShell } from '../entrar/page';

export default function Cadastro() {
  const router = useRouter();
  const [values, setValues] = useState({ nome: '', email: '', senha: '' });
  const [error, setError] = useState('');
  function update(field: keyof typeof values) { return (event: React.ChangeEvent<HTMLInputElement>) => setValues({ ...values, [field]: event.target.value }); }
  function submit(event: React.FormEvent) {
    event.preventDefault();
    if (!values.nome || !values.email || !values.senha) return setError('Todos os campos são obrigatórios.');
    if (!/^\S+@\S+\.\S+$/.test(values.email)) return setError('Informe um e-mail válido.');
    router.push('/app');
  }
  return <AuthShell title="Crie sua conta e comece"><form onSubmit={submit} noValidate><label>Nome<input aria-label="Nome" value={values.nome} onChange={update('nome')}/></label><label>E-mail<input aria-label="E-mail" value={values.email} onChange={update('email')} type="email"/></label><label>Senha<input aria-label="Senha" value={values.senha} onChange={update('senha')} type="password"/></label>{error && <p className="error" role="alert">{error}</p>}<button className="button utility-action" type="submit">Ir para minha análise <span>↗</span></button></form><p className="demo-notice">Ambiente de demonstração. Nenhum dado é armazenado.</p><p>Já tem uma conta? <Link href="/entrar">Entre</Link></p></AuthShell>;
}
