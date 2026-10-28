local state=Construction.newState(123)
local staged,seeds=ExpansionDemo.stage(state,123)
assert(staged and type(seeds)=='table','expansion demo did not stage')
assert(Construction.count(state)==0,'staging mutated original parcel')
local machines=0
for _,rec in pairs(staged.buildings)do
 if Catalog.types[rec.machineType].expansion then machines+=1 end
end
assert(machines==20 and Construction.count(staged)<=280)
local invalid,reason=ExpansionDemo.stage(staged,123)
assert(not invalid and reason=='expansion_requires_empty','demo overwrites populated factory')
local foreign=ExpansionDemo.stage(state,999)
assert(not foreign,'demo stages on another owner plot')
local testSession={state=staged,models={}}
Simulation.newSession(testSession)
for id,items in pairs(seeds)do testSession.runtime[id]={input={},output=table.clone(items),last=0,alternate=false,totalMade=0,totalMoved=0,nextRoute=0} end
for i=0,400 do clockNow=i*.6;Simulation.tick(testSession)end
for _,typ in ipairs(Catalog.expansionOrder)do
 local recipe=Catalog.recipes[Catalog.recipeId(typ)]
 for item in pairs(recipe.outputs)do assert(testSession.itemsSold[item]==12,'demo failed to deliver 12 '..item)end
end
assert(testSession.sales==240,'duplicate/lost cargo in new demo')
for _,slot in pairs(testSession.runtime)do assert(#slot.input==0 and #slot.output==0,'finite demo did not drain')end
print('PASS expansion demo stages atomically, respects ownership/empty plot, produces and sells 240 items on 20 independent lines')
