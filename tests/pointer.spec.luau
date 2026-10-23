-- Test the real coordinate adapter against Camera's documented API boundary.
local PointerRay = require('../src/client/PointerRay')
local camera = {}
function camera:ViewportPointToRay(x,y)
    return {coordinateSpace='device',x=x,y=y}
end
function camera:ScreenPointToRay(x,y)
    return {coordinateSpace='core',x=x,y=y}
end
local ray = PointerRay.fromScreen(camera,{X=320,Y=240},{X=0,Y=58})
assert(ray.coordinateSpace == 'core','inset-subtracted input must use ScreenPointToRay')
assert(ray.x == 320 and ray.y == 182,'pointer must preserve X and subtract only the declared inset')
ray = PointerRay.fromScreen(camera,{X=320,Y=240},{X=20,Y=0})
assert(ray.x == 300 and ray.y == 240,'horizontal safe inset must also be handled')
print('PASS pointer camera coordinate boundary (2 cases)')
