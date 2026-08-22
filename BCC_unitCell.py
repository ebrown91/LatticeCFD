import adsk.core, adsk.fusion, traceback, itertools

def build_and_export(box_size, cylinder_diameter, export_dir):
    app = adsk.core.Application.get()
    ui = app.userInterface

    doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
    design = adsk.fusion.Design.cast(app.activeProduct)
    rootComp = design.rootComponent

    radius = cylinder_diameter / 2.0

    # --- Box ---
    sketches = rootComp.sketches
    sketch = sketches.add(rootComp.xZConstructionPlane)
    sketchLines = sketch.sketchCurves.sketchLines
    startPoint = adsk.core.Point3D.create(0, 0, 0)
    endPoint = adsk.core.Point3D.create(box_size, box_size, 0)
    sketchLines.addTwoPointRectangle(startPoint, endPoint)
    prof = sketch.profiles.item(0)

    extrudes = rootComp.features.extrudeFeatures
    extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    extInput.setDistanceExtent(False, adsk.core.ValueInput.createByReal(box_size))
    extInput.isSolid = True
    ext = extrudes.add(extInput)
    body = ext.bodies.item(0)

    # --- Diagonal ---
    vertices = body.vertices
    pts = [v.geometry for v in vertices]
    p1, p2 = max(itertools.combinations(pts, 2), key=lambda pair: pair[0].distanceTo(pair[1]))

    diagSketch = rootComp.sketches.add(rootComp.xYConstructionPlane)
    diagSketch.is3D = True
    lines = diagSketch.sketchCurves.sketchLines
    diagLine = lines.addByTwoPoints(p1, p2)
    lineLength = diagLine.length

    planes = rootComp.constructionPlanes
    planeInput1 = planes.createInput()
    planeInput1.setByDistanceOnPath(diagLine, adsk.core.ValueInput.createByReal(0))
    plane1 = planes.add(planeInput1)

    # --- Circle + sweep ---
    circleSketch = rootComp.sketches.add(plane1)
    centerPoint = adsk.core.Point3D.create(0, 0, 0)
    circles = circleSketch.sketchCurves.sketchCircles
    circle = circles.addByCenterRadius(centerPoint, radius)
    profile = circleSketch.profiles.item(0)

    path = adsk.fusion.Path.create(diagLine, adsk.fusion.ChainedCurveOptions.noChainedCurves)
    sweeps = rootComp.features.sweepFeatures
    sweepInput = sweeps.createInput(profile, path, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    sweep = sweeps.add(sweepInput)
    cylinderBody = sweep.bodies.item(0)

    # --- Axis through top face center ---
    topFace = None
    maxZ = None
    for face in body.faces:
        if face.geometry.objectType == adsk.core.Plane.classType():
            normal = face.geometry.normal
            if abs(normal.z - 1.0) < 0.001:
                if maxZ is None or face.centroid.z > maxZ:
                    topFace = face
                    maxZ = face.centroid.z

    centroidPoint = topFace.centroid
    pointSketch = rootComp.sketches.add(topFace)
    skPoint = pointSketch.sketchPoints.add(pointSketch.modelToSketchSpace(centroidPoint))

    axes = rootComp.constructionAxes
    axisInput = axes.createInput()
    axisInput.setByPerpendicularAtPoint(topFace, skPoint)
    axis = axes.add(axisInput)

    # --- Circular pattern ---
    inputEntites = adsk.core.ObjectCollection.create()
    inputEntites.add(cylinderBody)

    circularFeats = rootComp.features.circularPatternFeatures
    circularFeatInput = circularFeats.createInput(inputEntites, axis)
    circularFeatInput.quantity = adsk.core.ValueInput.createByReal(4)
    circularFeatInput.totalAngle = adsk.core.ValueInput.createByString('360 deg')
    circularFeatInput.isSymmetric = False
    circularFeat = circularFeats.add(circularFeatInput)

    # --- Join copies (excluding duplicate original) ---
    toolBodies = adsk.core.ObjectCollection.create()
    for i in range(circularFeat.bodies.count):
        copyBody = circularFeat.bodies.item(i)
        if copyBody.entityToken != cylinderBody.entityToken:
            toolBodies.add(copyBody)

    combineFeatures = rootComp.features.combineFeatures
    joinInput = combineFeatures.createInput(cylinderBody, toolBodies)
    joinInput.operation = adsk.fusion.FeatureOperations.JoinFeatureOperation
    joinInput.isKeepToolBodies = False
    combineFeatures.add(joinInput)

    # --- Trim to box (intersect) ---
    toolBodiesBox = adsk.core.ObjectCollection.create()
    toolBodiesBox.add(body)
    trimInput = combineFeatures.createInput(cylinderBody, toolBodiesBox)
    trimInput.operation = adsk.fusion.FeatureOperations.IntersectFeatureOperation
    trimInput.isKeepToolBodies = True
    combineFeatures.add(trimInput)

    # --- Export ---
    exportMgr = design.exportManager
    filename = f'{export_dir}/box{box_size}_dia{cylinder_diameter}.stl'
    stlOptions = exportMgr.createSTLExportOptions(cylinderBody, filename)
    stlOptions.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementMedium
    exportMgr.execute(stlOptions)

    doc.close(False)  # close without saving


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        box_size = 5.0                              # single fixed box dimension
        diameters = [0.5, 1.0, 1.5, 2.0, 2.5]        # your parametric list
        export_dir = 'C:/Users/eebro/source/repos/LatticeCFD/stls/BCC'

        for d in diameters:
            build_and_export(box_size, d, export_dir)

        ui.messageBox(f'Done — exported {len(diameters)} files.')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))