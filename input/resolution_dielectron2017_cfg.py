import ROOT
def init_fun_sigma_BB():
    fun= ROOT.TF1('sigma_BB', '(x<[0])*(sqrt(([1]*[1]/x)+([2]*[2]/(x*x))+[3]*[3])+[4]*x)+(x>=[0])*([5]+[6]*x)')
    fun.SetParameter(0, 4.10000e+03)
    fun.SetParameter(1, 1.36248e+01)
    fun.SetParameter(2,-4.75855e-01)
    fun.SetParameter(3, 1.18957e+00)
    fun.SetParameter(4, 1.57269e-05)
    fun.SetParameter(5, 6.14990e-01)
    fun.SetParameter(6, 1.62551e-04)
    return fun
def init_fun_sigma_BE():
    fun= ROOT.TF1('sigma_BE', 'sqrt(([0]*[0]/x)+([1]*[1]/(x*x))+[2]*[2])+[3]*x')
    fun.SetParameter(0, 2.14720e+01)
    fun.SetParameter(1, 8.44088e-02)
    fun.SetParameter(2,-1.98193e+00)
    fun.SetParameter(3,-9.36303e-06)
    return fun
def init_fun_PowerL_BE():
    fun= ROOT.TF1('PowerL_BE', 'sqrt(([0]*[0]/x)+([1]*[1]/(x*x))+[2]*[2])+[3]*x')
    fun.SetParameter(0,-3.57044e+01)
    fun.SetParameter(1, 8.18668e-02)
    fun.SetParameter(2, 2.55223e-01)
    fun.SetParameter(3, 2.08919e-04)
    return fun
def init_fun_pol3_pol2(p0,p1,p2,p3,p4,p5):
    fun= ROOT.TF1('mean_BE', '(x<[0])*([1]+[2]*x+[3]*x*x)+(x>=[0])*([4]+[5]*x)')
    fun.SetParameter(0,p0)
    fun.FixParameter(0,p0)
    fun.SetParameter(1,p1)
    fun.SetParameter(2,p2)
    fun.SetParameter(3,p3)
    fun.SetParameter(4,p4)
    fun.SetParameter(5,p5)
    return fun
def init_fun_pol3_pol2_v1(p0,p1,p2,p3,p4,p5):
    fun= ROOT.TF1('mean_BE', '(x<[0])*([1]+[2]*x+[3]*x*x)+(x>=[0])*([4]+[5]*x)')
    fun.SetParameter(0,p0)
    fun.FixParameter(0,p0)
    fun.SetParameter(1,p1)
    fun.SetParameter(2,p2)
    fun.SetParameter(3,p3)
    fun.SetParameter(4,p4)
    fun.FixParameter(4,p4)
    fun.SetParameter(5,p5)
    return fun
def init_fun_line_pol3(p0,p1,p2,p3,p4):
    fun= ROOT.TF1('line4' , '(x<[0])*[1]+(x>=[0])*([2]+[3]*x+[4]*x*x)')
    fun.SetParameter(0,p0)
    fun.FixParameter(0,p0)
    fun.SetParameter(1,p1)
    fun.SetParameter(2,p2)
    fun.SetParameter(3,p3)
    fun.SetParameter(4,p4)
    return fun
def init_fun_pol2_pol2_pol1(p0,p1,p2,p3,p4,p5,p6):
    fun= ROOT.TF1('line4' , '(x<[0])*([1]+[2]*x)+(x>=[0] && x<=[3])*([4]+[5]*x)+(x>[3])*[6]')
    fun.SetParameter(0,p0)
    fun.FixParameter(0,p0)
    fun.SetParameter(1,p1)
    fun.SetParameter(2,p2)
    fun.SetParameter(3,p3)
    fun.FixParameter(3,p3)
    fun.SetParameter(4,p4)
    fun.SetParameter(5,p5)
    fun.SetParameter(6,p6)
    return fun
def init_fun_pol2_pol3_pol3(p0,p1,p2,p3,p4,p5,p6,p7,p8,p9):
    fun= ROOT.TF1('line4' , '(x<[0])*([1]+[2]*x)+(x>=[0] && x<=[3])*([4]+[5]*x+[6]*x*x)+(x>[3])*([7]+[8]*x+[9]*x*x)')
    fun.SetParameter(0,p0)
    fun.FixParameter(0,p0)
    fun.SetParameter(1,p1)
    fun.SetParameter(2,p2)
    fun.SetParameter(3,p3)
    fun.FixParameter(3,p3)
    fun.SetParameter(4,p4)
    fun.SetParameter(5,p5)
    fun.SetParameter(6,p6)
    fun.SetParameter(7,p7)
    fun.SetParameter(8,p8)
    fun.SetParameter(9,p9)
    return fun
def init_fun_pol3_pol2_pol1(p0,p1,p2,p3,p4,p5,p6,p7):
    fun= ROOT.TF1('line4' , '(x<[0])*([1]+[2]*x+[3]*x*x)+(x>=[0] && x<=[4])*([5]+[6]*x)+(x>[4])*[7]')
    fun.SetParameter(0,p0)
    fun.FixParameter(0,p0)
    fun.SetParameter(1,p1)
    fun.SetParameter(2,p2)
    fun.SetParameter(3,p3)
    fun.SetParameter(4,p4)
    fun.FixParameter(4,p4)
    fun.SetParameter(5,p5)
    fun.SetParameter(6,p6)
    fun.SetParameter(7,p7)
    return fun
def init_fun_pol2_pol3(p0,p1,p2,p3,p4,p5):
    fun= ROOT.TF1('line2' , '(x<[0])*([1]+[2]*x)+(x>=[0])*([3]+[4]*x+[5]*x*x)')
    fun.SetParameter(0,p0)
    fun.FixParameter(0,p0)
    fun.SetParameter(1,p1)
    fun.SetParameter(2,p2)
    fun.SetParameter(3,p3)
    fun.SetParameter(4,p4)
    fun.SetParameter(5,p5)
    return fun
    
def init_fun_line4(p0,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10):
    fun= ROOT.TF1('line4' , '(x<[0])*([1]+[2]*x)+(x>=[0] && x<=[3])*([4]+[5]*x)+(x>[3] && x<=[6])*([7]+[8]*x)+(x>[6])*([9]+[10]*x)')
    fun.SetParameter(0,p0)
    fun.FixParameter(0,p0)
    fun.SetParameter(1,p1)
    fun.SetParameter(2,p2)
    fun.SetParameter(3,p3)
    fun.FixParameter(3,p3)
    fun.SetParameter(4,p4)
    fun.SetParameter(5,p5)
    fun.SetParameter(6,p6)
    fun.FixParameter(6,p6)
    fun.SetParameter(7,p7)
    fun.SetParameter(8,p8)
    fun.SetParameter(9,p9)
    fun.SetParameter(10,p10)
    return fun

BB_sigma =init_fun_sigma_BB()
BE_sigma =init_fun_sigma_BE()
BB_mean  =init_fun_line4(4.50000e+02, 9.94975e-01, 4.46406e-06, 1.40000e+03, 9.96657e-01, 6.94260e-07, 4.00000e+03, 9.99176e-01,-1.04557e-06, 9.96035e-01,-2.61895e-07)
BE_mean  =init_fun_pol3_pol2(1.15000e+03, 9.93080e-01, 1.12739e-05,-5.52309e-09, 9.98370e-01, 4.03936e-07)
BB_PowerR=init_fun_line_pol3( 1.31700e+03, 4.96653e+01, 8.05790e+01,-2.59712e-02, 2.19637e-06)
BB_PowerL=init_fun_pol2_pol2_pol1( 3.60000e+02, 4.32594e+00,-6.72133e-03, 3.00000e+03, 1.98898e+00,-1.94021e-04, 1.41528e+00)
BB_CutL  =init_fun_pol3_pol2_pol1( 6.00000e+02, 8.87597e-01, 2.27228e-03,-1.77712e-06, 2.90000e+03, 1.56768e+00, 1.23681e-04, 1.94330e+00)
BB_CutR  =init_fun_line4( 3.00000e+02, 1.50257e+00, 1.17974e-03, 9.00000e+02, 1.81795e+00, 2.78018e-04, 3.00000e+03, 2.03203e+00, 3.11318e-05, 2.83146e+00,-2.37344e-04)
BE_PowerL=init_fun_PowerL_BE()
BE_PowerR=init_fun_pol2_pol3_pol3( 2.90000e+02, 1.04892e+02,-3.43043e-01, 2.91000e+03,-4.47534e+00, 2.41598e-02,-7.32975e-06,-2.64162e+02, 1.47964e-01,-1.92092e-05)
BE_CutL  =init_fun_pol3_pol2_v1( 2.20000e+03, 1.55663e+00, 6.09543e-04,-1.77418e-07, 2.20000e+00,-7.57247e-05)
BE_CutR  =init_fun_pol2_pol3( 1.05000e+03, 1.48018e+00, 4.82141e-03, 1.05329e+01,-3.83001e-03, 4.37797e-07)


class DCB_para:
    def __init__(self,name):
        self.name=name
        self.sigma =0 
        self.mean  =0 
        self.PowerL=0
        self.PowerR=0
        self.CutL  =0
        self.CutR  =0
    def get_value(self,mass,isBB):
        if isBB:
            self.sigma =BB_sigma .Eval(mass)/100
            self.mean  =BB_mean  .Eval(mass)-1
            self.PowerR=BB_PowerR.Eval(mass)
            self.PowerL=BB_PowerL.Eval(mass)
            self.CutL  =BB_CutL  .Eval(mass)
            self.CutR  =BB_CutR  .Eval(mass)
        else:
            self.sigma =BE_sigma .Eval(mass)/100
            self.mean  =BE_mean  .Eval(mass)-1
            self.PowerR=BE_PowerR.Eval(mass)
            self.PowerL=BE_PowerL.Eval(mass)
            self.CutL  =BE_CutL  .Eval(mass)
            self.CutR  =BE_CutR  .Eval(mass)
######### main #############
dCB=DCB_para("dcb")
dCB.get_value(1000,False) ##True for BB, False for BE
###### BCD parameter #############    
