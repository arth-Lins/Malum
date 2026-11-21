import {describe,it,expect,vi} from 'vitest'; import {render,screen,fireEvent} from '@testing-library/react';
vi.mock('next/navigation',()=>({useRouter:()=>({push:vi.fn()})})); vi.mock('next/link',()=>({default:({children,...p}:any)=><a {...p}>{children}</a>}));
import Cadastro from '../app/cadastro/page';
describe('Cadastro',()=>{it('indica campos obrigatórios',()=>{render(<Cadastro/>);fireEvent.click(screen.getByRole('button',{name:/ver planos/i}));expect(screen.getByRole('alert')).toHaveTextContent('Todos os campos');});});
