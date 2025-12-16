library(ggplot2)
library(wesanderson)

 
 # maindata<-read.csv("C:/Users/chenzhifei/Desktop/source/Experiments/avro_method_cover_main.csv", sep=",", header=FALSE)
 # yourkitdata<-read.csv("C:/Users/chenzhifei/Desktop/source/Experiments/avro_method_cover_yourkit.csv", sep=",", header=FALSE)
 # addata<-read.csv("C:/Users/chenzhifei/Desktop/source/Experiments/avro_method_cover_AD.csv", sep=",", header=FALSE)
 # asdata<-read.csv("C:/Users/chenzhifei/Desktop/source/Experiments/avro_method_cover_AS.csv", sep=",", header=FALSE)
 # dsdata<-read.csv("C:/Users/chenzhifei/Desktop/source/Experiments/avro_method_cover_DS.csv", sep=",", header=FALSE)
 # devdata<-read.csv("C:/Users/chenzhifei/Desktop/source/Experiments/avro_method_cover_dev.csv", sep=",", header=FALSE)

# maindata<-read.csv("C:/Users/chenzhifei/Desktop/source/Experiments/ivy_method_cover_main.csv", sep=",", header=FALSE)
# yourkitdata<-read.csv("C:/Users/chenzhifei/Desktop/source/Experiments/ivy_method_cover_yourkit.csv", sep=",", header=FALSE)
# addata<-read.csv("C:/Users/chenzhifei/Desktop/source/Experiments/ivy_method_cover_AD.csv", sep=",", header=FALSE)
# asdata<-read.csv("C:/Users/chenzhifei/Desktop/source/Experiments/ivy_method_cover_AS.csv", sep=",", header=FALSE)
# dsdata<-read.csv("C:/Users/chenzhifei/Desktop/source/Experiments/ivy_method_cover_DS.csv", sep=",", header=FALSE)
# devdata<-read.csv("C:/Users/chenzhifei/Desktop/source/Experiments/ivy_method_cover_dev.csv", sep=",", header=FALSE)


maindata<-read.csv("C:/Users/chenzhifei/Desktop/source/Experiments/pdfbox_method_cover_main.csv", sep=",", header=FALSE)
yourkitdata<-read.csv("C:/Users/chenzhifei/Desktop/source/Experiments/pdfbox_method_cover_yourkit.csv", sep=",", header=FALSE)
addata<-read.csv("C:/Users/chenzhifei/Desktop/source/Experiments/pdfbox_method_cover_AD.csv", sep=",", header=FALSE)
asdata<-read.csv("C:/Users/chenzhifei/Desktop/source/Experiments/pdfbox_method_cover_AS.csv", sep=",", header=FALSE)
dsdata<-read.csv("C:/Users/chenzhifei/Desktop/source/Experiments/pdfbox_method_cover_DS.csv", sep=",", header=FALSE)
devdata<-read.csv("C:/Users/chenzhifei/Desktop/source/Experiments/pdfbox_method_cover_dev.csv", sep=",", header=FALSE)

 
 # maindata<-read.csv("C:/Users/chenzhifei/Desktop/source/Experiments/cxf_method_cover_main.csv", sep=",", header=FALSE)
 # addata<-read.csv("C:/Users/chenzhifei/Desktop/source/Experiments/cxf_method_cover_AD.csv", sep=",", header=FALSE)
 # asdata<-read.csv("C:/Users/chenzhifei/Desktop/source/Experiments/cxf_method_cover_AS.csv", sep=",", header=FALSE)
 # dsdata<-read.csv("C:/Users/chenzhifei/Desktop/source/Experiments/cxf_method_cover_DS.csv", sep=",", header=FALSE)
 # devdata<-read.csv("C:/Users/chenzhifei/Desktop/source/Experiments/cxf_method_cover_dev.csv", sep=",", header=FALSE)
 

cols_cd<-c("red", "purple", "green", "orange", "blue")

df1<-data.frame(x=maindata$V1,y=maindata$V2,Type=as.factor("Our Approach"))
df3<-data.frame(x=addata$V1,y=addata$V2,Type=as.factor("Our Approach w/o SC"))
df4<-data.frame(x=asdata$V1,y=asdata$V2,Type=as.factor("Our Approach w/o DE"))
df5<-data.frame(x=dsdata$V1,y=dsdata$V2,Type=as.factor("Our Approach w/o AI"))
df6<-data.frame(x=devdata$V1,y=devdata$V2,Type=as.factor("Our Approach w/o Gen. Tests"))
ds<-rbind(df1, df3, df4, df5, df6)


ggplot(data=ds, aes(x, y, colour=ds$Type, linetype=ds$Type, size=ds$Type)) +
  # geom_line()+
  geom_smooth(method = "lm", se= FALSE, formula = y ~ poly(x, 15))+
  scale_linetype_manual(values=c("solid", "longdash", "longdash", "longdash", "longdash", "longdash"))+
  scale_size_manual(values=c(2,1,1,1,1))+  
  labs(x = "# of Methods in Top Optimization Spaces", y = "# of Actually Optimized Methods") +
  theme(axis.text.x=element_text(size=23, color="black"), 
        axis.text.y=element_text(size=23, color="black"),
        axis.title.x = element_text(size=20),
        axis.title.y = element_text(size=20),
        panel.background = element_blank(),
        panel.border = element_rect(colour="black",fill=NA),
        legend.text = element_text(size=20),
        legend.title = element_blank(),
        legend.key.size = unit(2, 'lines'),
        legend.position=c(0.02,0.98),legend.justification=c(0.02,0.98),
        legend.direction="vertical",
        legend.box.just = c("top"))+
  scale_x_continuous(limits = c(0,200))+
  # scale_y_continuous(limits = c(0,45))+
  scale_y_continuous(limits = c(0,75))+
  # scale_y_continuous(limits = c(0,22))+
  scale_colour_manual(values=cols_cd)