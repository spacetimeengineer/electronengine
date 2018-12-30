"""
ElectromagneticLab.py
By Michael.C Ryan
Description:
A Library of functions for building charge configurations and the fields they create.
Motivation:
To create a space or system for making valuable EM computations easily.
Application:
Mostly for research purposes.
Status:
This software is an on going project.
"""

import math 
from visual import *

"""
Description:
Creates a spherical charge object with a position vector, radius and charge density.
Example:
setCharge(vector(3,-43,23), 0.2, 1)
returns a spherically charged object positioned at <3, -43, 23> with a radius of 0.2 meters and 4.3 Coulombs/meter**3
Status:
Function is stable.
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
    #Defines the coulombs constant factor (newtons*meter**2/coulomb**2) which is to be used in any calculation of the electric field.
    coulombsConstant = 8.9875517873681764*10**9
    #Creates reference to the electric potential.
    electricPotential = 0
    #Loops through each chargeObject in the charge manifest.
    for chargeObject in chargeManifest:
        chargePositionVector = chargeObject[0].pos
        #Creates reference to the volume of the charge.
        volume=4.0/3.0*math.pi*chargeObject[0].radius**3
        #Creates reference to the charge density of the charge.
        chargeDensity = chargeObject[1]
        #Assigns reference to the value of charge.
        charge = chargeDensity*volume
        #So that the system will not attempt to divide by zero
        if getSeparationMagnitude(chargePositionVector, positionVector) != 0.0:
            #Uses superposition to construct an electric potential a a user defined position vector.
            electricPotential = electricPotential + charge/getSeparationMagnitude(chargePositionVector, positionVector)
            #Returns the electric potential.
    return coulombsConstant*electricPotential


"""
Description:
Returns the electric field vector in newtons/coulomb for a user defined position vector.
Example:
For Charges;
setCharge(vector(1,0,7), 0.01, 0.05) and setCharge(vector(-2,-3,1), 0.01, -0.05)
returns <-4.8033, -5.2517, -8.1491>
Status:
Function is stable.
"""
def getElectricField(positionVector):
    #Applies a cleaner reference to the euclidian coordinate system.
    X=0
    Y=1
    Z=2
    #Defines the coulombs constant factor (newtons*meter**2/coulomb**2) which is to be used in any calculation of the electric field.
    coulombsConstant = 8.9875517873681764*10**9
    #Creates empty electric field vector.
    electricField = vector(0,0,0)
    #Loops through every charge object available in the charge manifest.
    for chargeObject in chargeManifest:
        #Creates reference to the vector position of the charge in question.
        chargePositionVector = chargeObject[0].pos
        #Creates reference to the charges user defined volume (from radius).
        volume=4.0/3.0*math.pi*chargeObject[0].radius**3
        #Creates reference to the user defined property of charge density for the charge.
        chargeDensity = chargeObject[1]
        #Creates reference to the charge itself.
        charge = chargeDensity*volume
        #Creates reference to the distance between the charge and user defined position.
        separationVector = getSeparationVector(chargePositionVector, positionVector)
        #Creates reference to the separation distance between the charge and the user defined position.
        #(This is always used in electric field calculations.) 
        distance = getSeparationMagnitude(chargePositionVector, positionVector)
        #So that there ensure no division by zero.
        if distance != 0:
            #Creates refeence to the angle theta.
            theta = math.acos(separationVector[Z]/distance)
            #Creates refeence to the angle phi.
            phi = math.atan2(separationVector[Y],separationVector[X])
            #Creates reference to the magnitude of the electric field.
            magnitude = charge/distance**2
            #Uses superposition to compute the electric field components for the user defined point.
            electricField[X] = electricField[X] + math.sin(theta)*math.cos(phi)*magnitude
            electricField[Y] = electricField[Y] + math.sin(theta)*math.sin(phi)*magnitude
            electricField[Z] = electricField[Z] + math.cos(theta)*magnitude
        else:
            #Electric field is undefined at this point since the field is infinite.
            electricField = vector(float("inf"), float("inf"), float("inf"))
            #If the vector is not well defined.
    if electricField != vector(float("inf"), float("inf"), float("inf")):
        #Rounds the electric field vector components to the fourth decimal place.
        electricField[X]=round(coulombsConstant*electricField[X],4)
        electricField[Y]=round(coulombsConstant*electricField[Y],4)
        electricField[Z]=round(coulombsConstant*electricField[Z],4)
        #Returns electric field.
    return electricField    

"""
Description:

Example:

Status:
Not a stable function.
"""
def getForceFieldVector(chargeObject)
    
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
    #Array that stores the charge values with a sole intent to find the greatest charge available.
    chargeArray = []
    #Loops through all the charges available in the charge manifest.  
    for chargeObject in chargeManifest:
        #Creates reference to the volume of the charged object.
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
Not applicable.
Status:
Function is not stable.
"""
def drawSingleElectricFieldLine(beginCurve):
    #Applies a cleaner reference to the euclidian coordinate system.
    X=0
    Y=1
    Z=2
    #Defines the length of each electric field line segment.
    radialDifferential = 1
    #This array stores the points in euclidian space which define the curve.
    electricFieldLineArray=[]
    #This begin point is
    pointBegin = vector(beginCurve[X],beginCurve[Y],beginCurve[Z])
    #Appends position vectors into the electricFieldLineArray and will be used for plotting.
    electricFieldLineArray.append(pointBegin)
    #This defines how long each field line propogates away from it's origin.
    electricFieldLineLength = 30
    #Loops through the electric field line sections one by one.
    for electricFieldLineSection in range(electricFieldLineLength):
        pointEnd = getGreatestPotentialDropAdjacentPoint(pointBegin)
        #This (n-3)%20 == 1 term helps control where and also how often the field direction indicator cones become visible.
        if (electricFieldLineSection-3)%20 == 1:
            #Cone is created along the field line itself.
            cone(pos = pointBegin, axis = pointEnd-pointBegin, radius = 0.1, length = 0.7, color = color.red)
        #For each charge, check the the field lines are not multi-terminating at that location.
        for chargeObject in chargeManifest:
            #So that the field lines terminate cleanly at the negative charges, also so that less computation resources are used the lines are made to propigate as shortly as possible.
            if getSeparationMagnitude(pointEnd, chargeObject[0].pos)<=radialDifferential:
                #Breaks out of two for loops for the generation of a single electric field line.
                return curve(pos=electricFieldLineArray, color = color.red)
        electricFieldLineArray.append(pointEnd)
        #Now the old end point becomes the new begin point.
        pointBegin = pointEnd
    #Draws the electric field line.
    return curve(pos=electricFieldLineArray, color = color.red)

"""
Description:
Draws an electic field representation by applying a cone of variable radius,
length and direction to represent the electric field at that point it is visible.
Example:
Not applicable.
Status:
Function is not stable.
"""
def drawElectricVectorField():
    #Applies a cleaner reference to the euclidian coordinate system.
    X=0
    Y=1
    Z=2
    #Loops through every point in space to build an electric field vector representation.
    for x in range(-3,3,1):
        for y in range(-3,3,1):
            for z in range(-3,3,1):
                #Creates a reference to the position of the base of the cone.
                conePosition = vector(x,y,z)
                #Creates a reference to the position of the tip of the cone.
                greatestDropPoint = getGreatestPotentialDropAdjacentPoint(conePosition)
                #In order to define the geometry of the cone in an informatic way, the potential difference between the two points is considered. This makes sense since E=-del(V).
                potentialDifference = getElectricPotential(conePosition)-getElectricPotential(greatestDropPoint)
                #Creates cone object.
                cone(pos = conePosition, axis = greatestDropPoint-conePosition, radius = potentialDifference/20000, length = potentialDifference/5000, color = color.red)
    
"""
Description:
Returns the nearest point within a given accuracy of greatest potential drop.
This is how the system can calculate the paths of the field lines.
Example:
For Charges;
setCharge(vector(1,0,7), 0.01, 0.05) and setCharge(vector(-2,-3,1), 0.01, -0.05)
getGreatestPotentialDropAdjacentPoint(vector(3,6,-2))
returns <2.53806, 5.30866, -2.55557>
Status:
Function is stable.
"""
def getGreatestPotentialDropAdjacentPoint(positionVector):
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
            #These computations make use of the spherical to euclidian coordinate transformations.
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

setCharge(vector(1,0,7), 0.01, 0.05)
setCharge(vector(-2,-3,1), 0.01, -0.05)
setCharge(vector(2,-3,1), 0.01, 0.05)
setCharge(vector(-2,-3,1), 0.01, -0.05)
setCharge(vector(-2,3,1), 0.01, 0.05)
setCharge(vector(-2,-3,-11), 0.01, -0.05)

print getElectricField(vector(3,6,-2))

setElectricFieldLines()

"""
End Program
"""


