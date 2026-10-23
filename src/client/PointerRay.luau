-- Pointer coordinate boundary, isolated so the GUI-inset contract is testable.
local PointerRay = {}
function PointerRay.fromScreen(camera, position, inset)
    return camera:ScreenPointToRay(position.X-inset.X, position.Y-inset.Y)
end
return PointerRay
