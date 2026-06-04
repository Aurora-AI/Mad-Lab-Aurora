fallow --version exit_code=0
fallow --format json exit_code=0
fallow audit --format json --quiet exit_code=2
fallow dead-code --format json exit_code=1
fallow dupes --format json exit_code=0
fallow health --score --hotspots --targets --format json exit_code=0
fallow fix --dry-run --no-create-config --format json exit_code=0
git clone exit_code=128
