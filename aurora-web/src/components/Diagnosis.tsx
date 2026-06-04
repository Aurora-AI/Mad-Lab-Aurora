import React from 'react';

const Diagnosis: React.FC = () => {
  return (
    <section className="section-narrative bg-black-piano text-white-absolute">
      <div className="flex flex-col gap-12">
        <span className="font-mono text-xs tracking-[0.5em] text-zinc-500 uppercase">
          [ AUDIT_ID: 0x882A_SYST ]
        </span>
        <h2 className="text-monumental break-words leading-[0.75]">
          O SOFTWARE <br />
          MORREU.
        </h2>
        <div className="grid grid-cols-12 mt-12">
          <div className="col-span-12 md:col-span-8">
            <p className="text-editorial text-zinc-400">
              A era das ferramentas acabou. O mercado está saturado de soluções que penduram 
              em processos arcaicos. O que entregamos não é código; é a 
              <span className="text-white-absolute font-bold"> Infraestrutura Cognitiva </span> 
              que torna o erro matematicamente impossível.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Diagnosis;
