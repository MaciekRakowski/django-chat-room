def EclipseBreak():
      try:
        import sys
        #sys.path.append("/usr/local/google/home/maciekr/Software/eclipse/plugins/org.python.pydev_2.8.1.2013072611/pysrc")
        sys.path.append("C:\Software\eclipse\plugins\org.python.pydev_3.8.0.201409251235\pysrc")
        import pydevd;
        pydevd.settrace(trace_only_current_thread=False, suspend=False)  
      except:
        pass
EclipseBreak()