import math 
from visual import *

"""
Description:
Creates a spherical charge object with a position vector, radius and charge density.
Example:
setCharge(vector(3,-43,23), 0.2, 1)
returns a spherically charged object positioned at <3, -43, 23> with a radius of 0.2 meters and 4.3 Coulombs/meter**3
Status:
Function is not stable.
"""
def setCharge(positionVector, radius, chargeDensity):
    #Checks the charge sign to assign color to sphere.
    if chargeDensity < 0:
        chargeColor = color.blue
    if chargeDensity > 0:
        chargeColor = color.red
    if chargeDensity == 0:
        chargeColor = color.white
    #Creates geometric charge object.
    charge = sphere(pos=positionVector, radius=radius, color=chargeColor)
    #Stores this charge object in the electromagneticObjectManifest.
    chargeManifest.append([charge, chargeDensity])

"""
Description:
Returns the four potential value in volts*second/meter for a given position vector.
Example:

Status:
Function is not stable.
Function is not well defined.
"""
def getElectromagneticFourPotential(positionVector):
    return positionVector

"""
Description:
This function returns the separation vector between two vectors.
Example:
getSeparationVector(vector(2,6,1), vector(-4,5,32))
returns <-6, -1, 31>
Status:
Function is stable.
"""
def getSeparationVector(initialPosition, finalPosition):
    return finalPosition-initialPosition

"""
Description:
This function returns the separation magnitude between two vectors.
Example:
getSeparationMagnitude(vector(-32,6,10), vector(-4,-44,32))
returns 61.3840370129
Status:
Function is stable.
"""
def getSeparationMagnitude(initialPosition, finalPosition):
    return getSeparationVector(initialPosition, finalPosition).mag

"""
Description:
This function returns the voltage for a given position.
Example:
If only setCharge(vector(354,42,-456), 0.2, 0.00057321) and setCharge(vector(-45,34,45), 0.7, 0.00004535) were exectued,
then getElectricPotential(vector(-23,64,3))
returns 8417.88841135
Status:
Function is stable.
"""
def getElectricPotential(positionVector):
    coulombsConstant = 8.9875517873681764*10**9
    electricPotential = 0
    for chargeObject in chargeManifest:
        chargePositionVector = chargeObject[0].pos
        volume=4.0/3.0*math.pi*chargeObject[0].radius**3
        chargeDensity = chargeObject[1]
        charge = chargeDensity*volume
        #So that the system will not attempt to divide by zero
        if getSeparationMagnitude(chargePositionVector, positionVector) != 0.0:
            electricPotential = electricPotential + charge/getSeparationMagnitude(chargePositionVector, positionVector)
    return coulombsConstant*electricPotential


"""
Description:
Returns the electric field vector in newtons/coulomb for a given position vector.
Example:

Status:
Function is not stable.
"""
def getElectricField(positionVector):
    X=0
    Y=1
    Z=2
    coulombsConstant = 8.9875517873681764*10**9
    electricField = vector(0,0,0)
    for chargeObject in chargeManifest:
        chargePositionVector = chargeObject[0].pos
        volume=4.0/3.0*math.pi*chargeObject[0].radius**3
        chargeDensity = chargeObject[1]
        charge = chargeDensity*volume
        separationVector = getSeparationVector(chargePositionVector, positionVector)
        distance = getSeparationMagnitude(chargePositionVector, positionVector)
        if distance != 0:
            theta = math.acos(separationVector[Z]/distance)
            phi = math.atan2(separationVector[Y],separationVector[X])
            magnitude = charge/distance**2    
            electricField[X] = electricField[X] + math.sin(theta)*math.cos(phi)*magnitude
            electricField[Y] = electricField[Y] + math.sin(theta)*math.sin(phi)*magnitude
            electricField[Z] = electricField[Z] + math.cos(theta)*magnitude
        else:
            electricField = vector(float("inf"), float("inf"), float("inf"))
    if electricField != vector(float("inf"), float("inf"), float("inf")):
        electricField[X]=round(coulombsConstant*electricField[X],4)
        electricField[Y]=round(coulombsConstant*electricField[Y],4)
        electricField[Z]=round(coulombsConstant*electricField[Z],4)
    return electricField    

"""
Description:
Plots the electric field lines to the scene.
Example:
Not applicable since this has no return value.
Status:
Not a stable function.
"""
def setElectricFieldLines():
    #This defines the radius from the center point of the charge that the field line curve will begin.  
    increment = 0.1
    #This factor is nessecary when deailing with circles.
    rootHalfIncrement = math.sqrt(0.5)*increment
    #This factor is nessecary when deailing with spheres.
    rootThirdIncrement = math.sqrt(0.3333)*increment
    
    #Applies a cleaner reference to the euclidian coordinate system.
    X=0
    Y=1
    Z=2

    #Make 26 curves
    curveBeginSet=[]

    """
    Goal:
    To use the greatest charge available in the manifest in order to define how many field lines each charge gets.
    This way the density of electric field lines will correcty inform the viewer of the electric field magnitude.
    Ofcourse this is not a perfect representation since the lines are discrete and charge is not, however electric field lines
     were never meant to hold any REAL mathematical information.

    find the largest charge.  Say as a default we give this guy 14 lines and for every other charge we give them round(q/Q*14)
    """
    #Array that stores the charge values with a sole intent to find the greatest charge available.
    chargeArray = []
    radialDifferential = 1
    for chargeObject in chargeManifest:
        #Volume of the charged object.
        volume = 4.0/3.0*math.pi*chargeObject[0].radius**3
        #Charge of the charged object.
        charge = chargeObject[1]*volume
        #Appends charge so that they can be compared.
        chargeArray.append(charge)
    #Finds the charged object from the charge manifest which has the largest charge.        
    largestCharge = chargeManifest[chargeArray.index(max(chargeArray))]
    """
    We need to use this index to assign the cooresponding charge the greatest number of field lines.
    """
    for chargeObject in chargeManifest:
        chargeDensity = chargeObject[1]
        #If the charge is neutral
        if chargeDensity <= 0:
            pass
        else:
            #Calls the position of the charge.
            chargePositionVector=chargeObject[0].pos

            curveBeginSet.append([chargePositionVector[X]+increment, chargePositionVector[Y], chargePositionVector[Z]])
            curveBeginSet.append([chargePositionVector[X]-increment, chargePositionVector[Y], chargePositionVector[Z]])

            curveBeginSet.append([chargePositionVector[X], chargePositionVector[Y]+increment, chargePositionVector[Z]])
            curveBeginSet.append([chargePositionVector[X], chargePositionVector[Y]-increment, chargePositionVector[Z]])

            curveBeginSet.append([chargePositionVector[X], chargePositionVector[Y], chargePositionVector[Z]+increment])
            curveBeginSet.append([chargePositionVector[X], chargePositionVector[Y], chargePositionVector[Z]-increment])

            curveBeginSet.append([chargePositionVector[X]+rootThirdIncrement, chargePositionVector[Y]+rootThirdIncrement, chargePositionVector[Z]+rootThirdIncrement])
            curveBeginSet.append([chargePositionVector[X]-rootThirdIncrement, chargePositionVector[Y]-rootThirdIncrement, chargePositionVector[Z]+rootThirdIncrement])
            curveBeginSet.append([chargePositionVector[X]+rootThirdIncrement, chargePositionVector[Y]-rootThirdIncrement, chargePositionVector[Z]+rootThirdIncrement])
            curveBeginSet.append([chargePositionVector[X]-rootThirdIncrement, chargePositionVector[Y]+rootThirdIncrement, chargePositionVector[Z]+rootThirdIncrement])

            curveBeginSet.append([chargePositionVector[X]+rootThirdIncrement, chargePositionVector[Y]+rootThirdIncrement, chargePositionVector[Z]-rootThirdIncrement])
            curveBeginSet.append([chargePositionVector[X]-rootThirdIncrement, chargePositionVector[Y]-rootThirdIncrement, chargePositionVector[Z]-rootThirdIncrement])
            curveBeginSet.append([chargePositionVector[X]+rootThirdIncrement, chargePositionVector[Y]-rootThirdIncrement, chargePositionVector[Z]-rootThirdIncrement])
            curveBeginSet.append([chargePositionVector[X]-rootThirdIncrement, chargePositionVector[Y]+rootThirdIncrement, chargePositionVector[Z]-rootThirdIncrement])

            #For each electric field line for a given charge, there must be a path calculation point by point in order to
            #draw a smooth and accuarte visual representation of the eleectric field. 
            for beginCurve in curveBeginSet:
                #This array stores the points in euclidian space which define the curve.
                drawSingleElectricFieldLine(beginCurve)
        
"""
Description:
Draws a single electric field line from a positive charge.
Example:

Status:
Function is not stable.
"""
def drawSingleElectricFieldLine(beginCurve):
    X=0
    Y=1
    Z=2
    radialDifferential = 1
    #This array stores the points in euclidian space which define the curve.
    electricFieldLineArray=[]
    #This begin point is
    pointBegin = vector(beginCurve[X],beginCurve[Y],beginCurve[Z])
    electricFieldLineArray.append(pointBegin)
    for n in range(100):
        pointEnd = getGreatestPotentialDropAdjacentPoint(pointBegin)
        if (n-3)%20 == 1:
            cone(pos = pointBegin, axis = pointEnd-pointBegin, radius = 0.2, length = 1, color = color.red)
        for chargeObject in chargeManifest:
            if getSeparationMagnitude(pointEnd, chargeObject[0].pos)<=radialDifferential:
                #Breaks out of two for loops for the generation of a single electric field line.
                return curve(pos=electricFieldLineArray, color = color.red)
        electricFieldLineArray.append(pointEnd)
        pointBegin = pointEnd
        #label(pos=beginCurve, text='%0.1f V' % getElectricPotential(beginPoint))
    return curve(pos=electricFieldLineArray, color = color.red)

"""
Description:

Example:

Status:
Function is not stable.
"""
def drawelectricFieldVectorField():
    X=0
    Y=1
    Z=2
    for x in range(-3,3,1):
        for y in range(-3,3,1):
            for z in range(-3,3,1):
                conePosition = vector(x,y,z)
                greatestDropPoint = getGreatestPotentialDropAdjacentPoint(conePosition)
                potentialDifference = getElectricPotential(conePosition)-getElectricPotential(greatestDropPoint)
                cone(pos = conePosition, axis = greatestDropPoint-conePosition, radius = potentialDifference/20000, length = potentialDifference/5000, color = color.red)
    
    

"""
Description:
Returns the nearest point within a given accuracy of greatest potential drop.  This is how the system can calculate the paths of the field lines.
Example:

Status:
Function is stable.
"""
def getGreatestPotentialDropAdjacentPoint(positionVector):
    """
    The idea is to take a position vector and build a set a points around it with a set radius and angluar increment value, This will simplify the calculation
    makeing the software faster as well as giving smoother lines and greater control over the acuraccy to the user.
    """
    #This factor represents the amount of points on the curve of a circle which are to be analyzed.  The higher the number of points, the greater the accuracy of the field lines.
    thetaAngluarAccuracyFactor = 16
    #This factor represents the amount of points on the curve of a semi-circle which are to be analyzed.  The higher the number of points, the greater the accuracy of the field lines.
    phiAngluarAccuracyFactor = 2*thetaAngluarAccuracyFactor
    #This specifies the length of each strait line curve.  The smaller this factor is the more accurate the field lines become.
    radialDifferential = 1
    #This specifies the value of the angular dispacement.  For example an anglularAccuracyFactor of 16 will mean that each angular dispacement is pi/8 radians.
    angularDifferential = math.pi/thetaAngluarAccuracyFactor
    #For each point analyzed, the potential at those points will be stored ot be compared.  Eventually the point of highest or lowest potential will be picked.
    potentialPointSet=[]
    for n in range(thetaAngluarAccuracyFactor):
        #Theta can take on values [0,pi].
        for m in range(phiAngluarAccuracyFactor):
            #Theta can take on values [0,pi].
            theta = n*angularDifferential
            #Phi can take on values [0,2*pi].
            phi = m*angularDifferential
            #Applies the spherical to euclidian coordinate transformations.
            x=radialDifferential*math.sin(theta)*math.cos(phi)
            y=radialDifferential*math.sin(theta)*math.sin(phi)
            z=radialDifferential*math.cos(theta)
            #if its the first point in question then it must be the lowest potential difference point sofar.
            if (n == 0 & m == 0):
                #Assigns this comparison variable to the potential difference of the first point.
                lowestPotential = getElectricPotential(positionVector+vector(x,y,z))
                #Sets point to the lowest potential point.
                lowestPotentialPoint = positionVector+vector(x,y,z)
            else:
                #If the potential drop for this point is lower than any other point we have computed then this is the new lowest potential point.
                if getElectricPotential(positionVector+vector(x,y,z)) < lowestPotential:
                    #Assigns this comparison variable to the potential difference of this new point.
                    lowestPotential = getElectricPotential(positionVector+vector(x,y,z))
                    #Sets point to the lowest potential point.
                    lowestPotentialPoint = positionVector+vector(x,y,z)
    #Returns the point which is closest to the point of greatest potential drop.
    return lowestPotentialPoint
                

"""
Begin Program
"""


global chargeManifest
chargeManifest=[]

setCharge(vector(0,0,0), 0.01, 0.05)

drawelectricFieldVectorField()
setElectricFieldLines()

"""
End Program
"""


