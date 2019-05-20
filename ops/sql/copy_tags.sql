# This file is for reference.  Don't run it as a script.

##############
# Tags
##############

COPY tag (tag_name) FROM STDIN WITH CSV;

# paste in tag.csv...

##############
# Associations
##############

COPY eip_tag (eip_id, tag_name) FROM STDIN WITH CSV;

# paste in eip_tag.csv...
