library(stats)
library(effsize)




process <- function(data)
{
    xC = ncol(data)
    xR = nrow(data)

    before <- c(0)
    after <- c(0)

    for (c in 1:xR)
    {
        before[c] = data[c, xC-1]
        after[c] = data[c, xC]
    }

    p_result = wilcox.test(before, after, paired = TRUE, alternative = "greater")$p.value
    delta_result = cliff.delta(before, after)$estimate

    print (p_result)
    print (delta_result)

}

files <- c(
"C:\\Users\\chenzhifei\\Desktop\\source\\subjects\\avro\\score_seed_changes_avro-1.6.0_avro-1.8.1.csv",
"C:\\Users\\chenzhifei\\Desktop\\source\\subjects\\avro\\score_pattern_changes_avro-1.6.0_avro-1.8.1.csv",
"C:\\Users\\chenzhifei\\Desktop\\source\\subjects\\ivy\\score_seed_changes_ivy-2.0.0-2009.1_ivy-2.4.0-2014.12.csv",
"C:\\Users\\chenzhifei\\Desktop\\source\\subjects\\ivy\\score_pattern_changes_ivy-2.0.0-2009.1_ivy-2.4.0-2014.12.csv",
"C:\\Users\\chenzhifei\\Desktop\\source\\subjects\\pdfbox\\score_seed_changes_pdfbox-1.8.4-2014.1_pdfbox-2.0.4-2016.12.csv",
"C:\\Users\\chenzhifei\\Desktop\\source\\subjects\\pdfbox\\score_pattern_changes_pdfbox-1.8.4-2014.1_pdfbox-2.0.4-2016.12.csv"

)

for (f in 1:6){
    name = files[f]
    print (name)
    data <- read.table(name, skip=1, sep=",", na.strings=" ")
    process(data)
}