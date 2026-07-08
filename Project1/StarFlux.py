import numpy as np
import matplotlib.pyplot as plt
import astropy.io.fits
import astropy.stats
from astropy.stats import sigma_clipped_stats
from astropy.stats import sigma_clip
from photutils.detection import DAOStarFinder
from photutils.aperture import CircularAperture
from photutils.aperture import aperture_photometry

#Loading in the fits file
fits = astropy.io.fits.open("Vcomb.fits")
picData = fits[0].data
fits.close()

#checking for outlier data using sigma clipping
mean, median, std = astropy.stats.sigma_clipped_stats(picData, sigma_lower = 2, 
sigma_upper = 5)
clippedData = sigma_clip(picData, sigma_lower = 1, sigma_upper = 20)
no_outliers = np.sum(clippedData.mask)

#Using DAOStarFinder to detect stars, and highlighting them with the circular aperture
daofind = DAOStarFinder(fwhm = 20, threshold = 5 * std)
sources = daofind(clippedData - median)
positions = np.transpose((sources['xcentroid'], sources['ycentroid']))
apertures = CircularAperture(positions, r = 10)
#finding flux in the star apertures encircled above using aperture photometry
phot_table = aperture_photometry(clippedData, apertures)
fluxes = phot_table['aperture_sum']


# Plot histogram of fluxes
plt.figure(figsize=(10, 6))
plt.hist(fluxes, bins=50, color='purple', alpha=0.7, edgecolor='black', density = False)
plt.xlabel('Flux (counts)')
plt.ylabel('Number of Stars')
plt.title('Histogram of Detected Star Fluxes in Messier 12')
plt.grid(True)
plt.show()

# Plot histogram of relative fluxes
plt.figure(figsize=(10, 6))
plt.hist(fluxes, bins=50, color='purple', alpha=0.7, edgecolor='black', density = True)
plt.xlabel('Flux (counts)')
plt.ylabel('Proportion of Stars')
plt.title('Histogram of Detected Star Fluxes in Messier 12')
plt.grid(True)
plt.show()
