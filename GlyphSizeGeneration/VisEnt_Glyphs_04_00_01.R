library( pracma )


#
# Setup the array describing each signal output
#
coefs = matrix(1:8, 8, 12)
colnames(coefs) <-c( "freq1","freq2", "freq3", 
                 "phase1", "phase2", "phase3", 
                 "amp1", "amp2", "amp3", "amp4", "Rsignal","wave")

coefs[1,] <-c(4,8,0, 0,0,0 ,0.8,0,0,0,0.65,1) #Square wave
coefs[2,] <-c(0,0,0, 0,0,0, 0,0,0,0,0.8,0) #Sine waves
coefs[3,] <-c(3,0,0, 0,0,0, 0.18,0,0,0,0.8,0)
coefs[4,] <-c(6,0,0, 0,0,0, 0.18,0,0,0,0.8,0)
coefs[5,] <-c(12,0,0, 0,0,0, 0.18,0,0,0,0.8,0)
coefs[6,] <-c(24,0,0 ,0,0,0, 0.18,0,0,0,0.8,0)
coefs[7,] <-c(48,0,0 ,0,0,0, 0.18,0,0,0,0.8,0)
coefs[8,] <-c(96,0,0 ,0,0,0, 0.18,0,0,0,0.8,0)

#Shape generating functions for harmonic circle plots
computeShapeX<-function(f1,freq2,freq3,phase1,phase2,phase3,
                        amp1,amp2,amp3,amp4)
{
  (Rsignal+amp1*sin(f1*t+phase1) + 
     amp2*sin(freq2*t+phase2) + 
     amp3*sin(freq3*t+phase3) + 
     amp4 * noiseG ) * cos(t)  
}

computeBase<-function(freq1,freq2,freq3,phase1,phase2,phase3,
                        amp1,amp2,amp3,amp4)
{
  (Rsignal+amp1*sin(freq1*t+phase1) + 
     amp2*sin(freq2*t+phase2) + 
     amp3*sin(freq3*t+phase3) + 
     amp4 * noiseG )
}

computeShapeY<-function(freq1,freq2,freq3,phase1,phase2,phase3,
                        amp1,amp2,amp3,amp4)
{
  (Rsignal+amp1*sin(freq1*t+phase1) + 
     amp2*sin(freq2*t+phase3)+ 
     amp3*sin(freq3*t+phase3) + 
     amp4 * noiseG ) * sin(t)
}

#Shape generating functions for sqaure wave circle plots
computeSquareX<-function(freq1,freq2,freq3,phase1,phase2,phase3,
                        amp1,amp2,amp3,amp4)
{
  (Rsignal+ ceiling(amp1*sin(freq1*t+phase1) + 
     amp2*sin(freq2*t+phase2) + 
     amp3*sin(freq3*t+phase3) + 
     amp4 * noiseG)/2.4 -0.1) * cos(t)
}

computeSquareY<-function(freq1,freq2,freq3,phase1,phase2,phase3,
                        amp1,amp2,amp3,amp4)
{
  (Rsignal+ ceiling(amp1*sin(freq1*t+phase1) + 
     amp2*sin(freq2*t+phase3)+ 
     amp3*sin(freq3*t+phase3) + 
     amp4 * noiseG)/2.4 -0.1) * sin(t)
}

squareBase<-function(freq1,freq2,freq3,phase1,phase2,phase3,
                         amp1,amp2,amp3,amp4)
{
  (Rsignal+ ceiling(amp1*sin(freq1*t+phase1) + 
                      amp2*sin(freq2*t+phase2) + 
                      amp3*sin(freq3*t+phase3) + 
                      amp4 * noiseG)/2.4 -0.1)
}

harmonicComponents <- function(freq1,freq2,freq3,phase1,phase2,phase3,
                            amp1,amp2,amp3,amp4 )
{
  return( list( "x" = computeShapeX(freq1,freq2,freq3,
                     phase1,phase2,phase3,
                     amp1,amp2,amp3,amp4),
        "y" = computeShapeY(freq1,freq2,freq3,
                     phase1,phase2,phase3,
                     amp1,amp2,amp3,amp4),
        "base" = computeBase(freq1,freq2,freq3,
                    phase1,phase2,phase3,
                    amp1,amp2,amp3,amp4) ) )
}

squareComponents <- function(freq1,freq2,freq3,phase1,phase2,phase3,
                             amp1,amp2,amp3,amp4 )
{
  return( list( "x" = computeSquareX(freq1,freq2,freq3,
                                     phase1,phase2,phase3,
                                     amp1,amp2,amp3,amp4),
                "y" = computeSquareY(freq1,freq2,freq3,
                                     phase1,phase2,phase3,
                                     amp1,amp2,amp3,amp4),
                "base" = squareBase(freq1,freq2,freq3,
                                    phase1,phase2,phase3,
                                    amp1,amp2,amp3,amp4) ) )
}

plotSignal <- function( x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, t, base5){
  fileName <- paste( sprintf("%02d-", freq1),
                        sprintf("%02d-", freq2),
                        sprintf("%02d-", freq3),
                        sprintf("%01d", (amp4 >0) ), sep="" )
  name <- paste("Type: ", fileName )

  plot(x,y, type="l", asp=1, col = gridcol,
       main = name )
  abline(h=0, v=0, col = gridcol )
  lines(x1,y1, type="l", col = gridcol )
  lines(x2,y2, type="l", col = gridcol )
  lines(x3,y3, type="l", col = gridcol )
  lines(x4,y4, type="l", col = gridcol )
  lines(x5,y5, type="l", col = "olivedrab", lwd = 2 )
  
  #SampeEn parameters
  n = 2
  r = 0.2
  
  SampEn <- sample_entropy( base5, n, r ) 
  name = paste("SampEnt: ", sprintf("%2.2f", SampEn) )
  plot( t, base5, type="l", col = "olivedrab",main = name )
  
  return ( fileName )
}


#
#Sampling points around the circle
#
N <- 720
zeros <- rep(0,N)
seq <- (1:N)
step <- 2*pi/N # step for the sine wave.

gridcol = "lightpink"

#Sine wave - smooth but varying
sinWave <- sin(step*seq)
cosWave <- cos(step*seq)

#Radii of signal and grid
Rsignal <- 0.6
r1 <- 1.0
r2 <- 0.8
r3 <- 0.6
r4 <- 0.4
r5 <- 0.2

noiseU <- runif(N,-1,1) # Uniform noise
noiseG <- rnorm(N,-0.6,0.6) # Gaussian noise

#theta sequence of angles
t <- step*seq

x = r1 * cos(t)
y = r1 * sin(t)

x1 = r2 * cos(t)
y1 = r2 * sin(t)

x2 = r3 * cos(t)
y2 = r3 * sin(t)

x3 = r4 * cos(t)
y3 = r4 * sin(t)

x4 = r5 * cos(t)
y4 = r5 * sin(t)

x5 <- vector()
y5 <- vector()
base5<-vector()

freq1 <-0
freq2 <- 0
freq3 <- 0
phase1 <- 0.0*2*pi
phase2 <- 0.0*2*pi
phase3 <- 0.0*2*pi
amp1 <- 0.00
amp2 <- 0.00
amp3 <- 0.00
amp4 <- 0.00
components <- vector()

for( i in 1:nrow(coefs)) {
  Rsignal <- coefs[i,"Rsignal"]
  if ( coefs[i,"wave"] == 0) {
    freq1 <<-coefs[i,"freq1"]
    freq2 <<- coefs[i,"freq2"]
    freq3 <<- coefs[i,"freq3"]
    phase1 <<- coefs[i,"phase1"]*2*pi
    phase2 <<- coefs[i,"phase2"]*2*pi
    phase3 <<- coefs[i,"phase3"]*2*pi
    amp1 <<- coefs[i,"amp1"]
    amp2 <<- coefs[i,"amp2"]
    amp3 <<- coefs[i,"amp3"]
    amp4 <<- coefs[i,"amp4"]
    components <<- harmonicComponents(freq1,freq2,freq3,
                                    phase1,phase2,phase3,
                                    amp1,amp2,amp3,amp4 )
  }
  else
  {
    freq1 <<-coefs[i,"freq1"]
    freq2 <<- coefs[i,"freq2"]
    freq3 <<- coefs[i,"freq3"]
    phase1 <<- coefs[i,"phase1"]*2*pi
    phase2 <<- coefs[i,"phase2"]*2*pi
    phase3 <<- coefs[i,"phase3"]*2*pi
    amp1 <<- coefs[i,"amp1"]
    amp2 <<- coefs[i,"amp2"]
    amp3 <<- coefs[i,"amp3"]
    amp4 <<- coefs[i,"amp4"]    
    components <<- squareComponents(freq1,freq2,freq3,
                                    phase1,phase2,phase3,
                                    amp1,amp2,amp3,amp4 )    
  }
  
  x5 <- components$x
  y5 <- components$y
  base5 <- components$base
  
  par(mfrow=c(1,2))
  
  baseName<-plotSignal( x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, t, base5)
  
  verts <- cbind( x5, y5, zeros )
  fileName <- paste( "sgnl",baseName,".csv", sep="" )
  print( fileName )
  write.csv(verts,fileName)
  
  par(mfrow=c(1,1) )
  imageFileName <- paste( "sgnl",baseName,".png", sep="" )
  svgFileName <- paste( "sgnl",baseName,".svg", sep="" )
  plot(x,y, type="l", asp=1, col = gridcol, main = imageFileName )
  polygon(x5,y5,col="black")
  dev.copy(png, imageFileName)
  dev.copy(svg, svgFileName)
  dev.off()

}

stop( "Successful file write out" )
