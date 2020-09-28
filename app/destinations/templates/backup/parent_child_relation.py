
 _Fit__projectedFits : relation(Fit,
                                  primaryjoin = child.c.victimid == parent.c.id,
                                  secondaryjoin = parent.c.id == child.c.id,
                                  secondary = child,
                                  collection_class = HandledProjectedFitList),
 _Fit__projectedOnto : relation(Fit,
                                  primaryjoin = parent.c.id == child.c.id,
                                  secondaryjoin = parent.c.id == child.c.victimid == parent.c.id,
                                  secondary = child,
                                  collection_class = HandledProjectedFitList)