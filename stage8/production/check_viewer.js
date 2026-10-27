// Exercise graph selection without a browser; visual layout still needs a browser check.
const fs=require('fs'),vm=require('vm'),assert=require('assert');
const path=require('path'),dir=__dirname;
const page=fs.readFileSync(path.join(dir,'ABRIR_Arbol_Produccion.html'),'utf8');
const script=page.split('<script>')[1].split('</script>')[0];
function element(dataset={}){const classes=new Set();return {dataset,value:'',innerHTML:'',children:[],handlers:{},classList:{toggle(c,on){if(on)classes.add(c);else classes.delete(c)},remove(c){classes.delete(c)},contains(c){return classes.has(c)}},append(o){this.children.push(o)},addEventListener(k,fn){this.handlers[k]=fn}}}
const nodes=[...page.matchAll(/class="node" data-id="([^"]+)"/g)].map(m=>element({id:m[1]}));
const edges=[...page.matchAll(/class="edge" data-from="([^"]+)" data-to="([^"]+)"/g)].map(m=>element({from:m[1],to:m[2]}));
const select=element(),details=element(),all=element();
const document={createElement:()=>element(),querySelector:s=>({'#resource':select,'#details':details,'#all':all})[s],querySelectorAll:s=>s==='.node'?nodes:s==='.edge'?edges:s==='[data-item]'?[]:s==='.dim,.selected'?[...nodes,...edges].filter(n=>n.classList.contains('dim')||n.classList.contains('selected')):[]};
const ctx=vm.createContext({document});vm.runInContext(script,ctx);
assert.equal(select.children.length,14);
for(const [item,expected] of [['Ingot',['RawMatter','Carbon','Iron','BaseMetal','SyntheticOre','Ingot']],['BasicCrystal',['RawMatter','Oxygen','Silicon','Silicate','BasicCrystal']],['Hydrogen',['RawMatter','Hydrogen']]]){
 vm.runInContext(`show('${item}')`,ctx);
 assert.deepEqual(nodes.filter(n=>!n.classList.contains('dim')).map(n=>n.dataset.id).sort(),expected.sort());
 assert.equal(select.value,item);assert(details.innerHTML.includes('Ingredientes'));
}
select.value='ConductiveMix';select.handlers.change();assert(details.innerHTML.includes('Cobre ×1')&&details.innerHTML.includes('Silicio ×1'));
let prevented=false;nodes.find(n=>n.dataset.id==='Ingot').handlers.keydown({key:'Enter',preventDefault(){prevented=true}});assert(prevented&&select.value==='Ingot');
all.handlers.click();assert(nodes.every(n=>!n.classList.contains('dim')));assert.equal(select.value,'');
console.log('PASS viewer: dependency selection, recipe details, selector, keyboard and reset (DOM adapter)');
