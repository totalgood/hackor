#  Oct 6, 2015
#  HACK Oregon

# DATA from: http://totalgood.github.io/hackor/

# read
x <-read.csv("raw_committee_transactions.csv")
head(x)
str(x)

## fields most interested in today:
#  filer_id, amount, tran_date


# for each filer_id, sum up amount
x1 <- aggregate(x$amount, list(filer_id=x$filer_id),sum)

# clean up the field names (must be better way!)
str(x1)
names(x1) <- c('filer_id','amount_total')

# field names now correct, but sorted by filer_id
head(x1)


# use plyr package

library(plyr)
# sort, look at first 6, these are smallest totals
head(arrange(x1,amount_total))

# try, and we see filer_id=17015 has largest
tail(arrange(x1,amount_total))


# So, return to dataframe x, and make a subset with  EVERY each amount for each tran_date (for filer_id='17015')
# call this big

big <- x[x$filer_id=='17015',]
head(big) # seems ok
unique(big$filer_id) # just to sure, only 1 filer_id (17015)
str(big)

# what we want is, sum for EACH tran_date (for filer_id='17015')
big_by_date <- aggregate(big,amount, list(big$tran_date),sum)
# just a check on field classes
lapply(big_by_date,class)

big_by_date # looks right, expect 'x' has become field name for daily totals (fix!)
# plot looks ugly, because donations are compressed on graph
plot(big_by_date$tran_date,big_by_date$x)

#NEXT:   use ggplot




