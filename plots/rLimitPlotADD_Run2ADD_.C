{
//=========Macro generated from canvas: cCL/cCL
//=========  (Thu Feb 14 09:16:13 2019) by ROOT version5.34/18
   TCanvas *cCL = new TCanvas("cCL", "cCL",0,0,800,500);
   gStyle->SetOptStat(0);
   cCL->SetHighLightColor(2);
   cCL->Range(0,0,1,1);
   cCL->SetFillColor(0);
   cCL->SetBorderMode(0);
   cCL->SetBorderSize(2);
   cCL->SetTickx(1);
   cCL->SetTicky(1);
   cCL->SetFrameBorderMode(0);
  
// ------------>Primitives in pad: plotPad
   TPad *plotPad = new TPad("plotPad", "plotPad",0,0,1,1);
   plotPad->Draw();
   plotPad->cd();
   plotPad->Range(3562.5,-1,7937.5,9);
   plotPad->SetFillColor(0);
   plotPad->SetBorderMode(0);
   plotPad->SetBorderSize(2);
   plotPad->SetFrameBorderMode(0);
   plotPad->SetFrameBorderMode(0);
   
   TH1F *DummyGraph = new TH1F("DummyGraph","",100,4000,7500);
   DummyGraph->SetMinimum(0);
   DummyGraph->SetMaximum(8);
   DummyGraph->SetStats(0);

   Int_t ci;   // for color index setting
   ci = TColor::GetColor("#000099");
   DummyGraph->SetLineColor(ci);
   DummyGraph->GetXaxis()->SetTitle("#Lambda [GeV]");
   DummyGraph->GetXaxis()->SetRange(1,100);
   DummyGraph->GetXaxis()->SetLabelFont(42);
   DummyGraph->GetXaxis()->SetTitleSize(0.045);
   DummyGraph->GetXaxis()->SetTitleFont(42);
   DummyGraph->GetYaxis()->SetTitle("95% CL limit on signal strength #mu");
   DummyGraph->GetYaxis()->SetLabelFont(42);
   DummyGraph->GetYaxis()->SetTitleSize(0.045);
   DummyGraph->GetYaxis()->SetTitleFont(42);
   DummyGraph->GetZaxis()->SetLabelFont(42);
   DummyGraph->GetZaxis()->SetLabelSize(0.035);
   DummyGraph->GetZaxis()->SetTitleSize(0.035);
   DummyGraph->GetZaxis()->SetTitleFont(42);
   DummyGraph->Draw("");
   
   TGraphAsymmErrors *grae = new TGraphAsymmErrors(16);
   grae->SetName("Graph0");
   grae->SetTitle("Graph");

   ci = TColor::GetColor("#ffcc00");
   grae->SetFillColor(ci);
   grae->SetPoint(0,4000,0.01994397);
   grae->SetPointError(0,0,0,0,0);
   grae->SetPoint(1,4500,0.06041577);
   grae->SetPointError(1,0,0,0,0);
   grae->SetPoint(2,5000,0.1488363);
   grae->SetPointError(2,0,0,0,0);
   grae->SetPoint(3,5500,0.3521872);
   grae->SetPointError(3,0,0,0,0);
   grae->SetPoint(4,6000,0.832963);
   grae->SetPointError(4,0,0,0,0);
   grae->SetPoint(5,6500,2.591884);
   grae->SetPointError(5,0,0,0,0);
   grae->SetPoint(6,7000,8.29858);
   grae->SetPointError(6,0,0,0,0);
   grae->SetPoint(7,7500,8.940813);
   grae->SetPointError(7,0,0,0,0);
   grae->SetPoint(8,7500,9.668129);
   grae->SetPointError(8,0,0,0,0);
   grae->SetPoint(9,7000,9.561251);
   grae->SetPointError(9,0,0,0,0);
   grae->SetPoint(10,6500,5.906512);
   grae->SetPointError(10,0,0,0,0);
   grae->SetPoint(11,6000,1.924513);
   grae->SetPointError(11,0,0,0,0);
   grae->SetPoint(12,5500,0.772963);
   grae->SetPointError(12,0,0,0,0);
   grae->SetPoint(13,5000,0.3851066);
   grae->SetPointError(13,0,0,0,0);
   grae->SetPoint(14,4500,0.1605509);
   grae->SetPointError(14,0,0,0,0);
   grae->SetPoint(15,4000,0.06896876);
   grae->SetPointError(15,0,0,0,0);
   
   TH1F *Graph_Graph1 = new TH1F("Graph_Graph1","Graph",100,3650,7850);
   Graph_Graph1->SetMinimum(0);
   Graph_Graph1->SetMaximum(10.63295);
   Graph_Graph1->SetDirectory(0);
   Graph_Graph1->SetStats(0);

   ci = TColor::GetColor("#000099");
   Graph_Graph1->SetLineColor(ci);
   Graph_Graph1->GetXaxis()->SetLabelFont(42);
   Graph_Graph1->GetXaxis()->SetLabelSize(0.035);
   Graph_Graph1->GetXaxis()->SetTitleSize(0.035);
   Graph_Graph1->GetXaxis()->SetTitleFont(42);
   Graph_Graph1->GetYaxis()->SetLabelFont(42);
   Graph_Graph1->GetYaxis()->SetLabelSize(0.035);
   Graph_Graph1->GetYaxis()->SetTitleSize(0.035);
   Graph_Graph1->GetYaxis()->SetTitleFont(42);
   Graph_Graph1->GetZaxis()->SetLabelFont(42);
   Graph_Graph1->GetZaxis()->SetLabelSize(0.035);
   Graph_Graph1->GetZaxis()->SetTitleSize(0.035);
   Graph_Graph1->GetZaxis()->SetTitleFont(42);
   grae->SetHistogram(Graph_Graph1);
   
   grae->Draw("f");
   
   grae = new TGraphAsymmErrors(16);
   grae->SetName("Graph1");
   grae->SetTitle("Graph");

   ci = TColor::GetColor("#00cc00");
   grae->SetFillColor(ci);
   grae->SetPoint(0,4000,0.02771211);
   grae->SetPointError(0,0,0,0,0);
   grae->SetPoint(1,4500,0.07339209);
   grae->SetPointError(1,0,0,0,0);
   grae->SetPoint(2,5000,0.1712914);
   grae->SetPointError(2,0,0,0,0);
   grae->SetPoint(3,5500,0.3818336);
   grae->SetPointError(3,0,0,0,0);
   grae->SetPoint(4,6000,0.9020821);
   grae->SetPointError(4,0,0,0,0);
   grae->SetPoint(5,6500,2.732234);
   grae->SetPointError(5,0,0,0,0);
   grae->SetPoint(6,7000,8.385193);
   grae->SetPointError(6,0,0,0,0);
   grae->SetPoint(7,7500,8.987355);
   grae->SetPointError(7,0,0,0,0);
   grae->SetPoint(8,7500,9.500025);
   grae->SetPointError(8,0,0,0,0);
   grae->SetPoint(9,7000,9.286272);
   grae->SetPointError(9,0,0,0,0);
   grae->SetPoint(10,6500,4.491895);
   grae->SetPointError(10,0,0,0,0);
   grae->SetPoint(11,6000,1.406074);
   grae->SetPointError(11,0,0,0,0);
   grae->SetPoint(12,5500,0.6215669);
   grae->SetPointError(12,0,0,0,0);
   grae->SetPoint(13,5000,0.2858747);
   grae->SetPointError(13,0,0,0,0);
   grae->SetPoint(14,4500,0.1227476);
   grae->SetPointError(14,0,0,0,0);
   grae->SetPoint(15,4000,0.05171529);
   grae->SetPointError(15,0,0,0,0);
   
   TH1F *Graph_Graph2 = new TH1F("Graph_Graph2","Graph",100,3650,7850);
   Graph_Graph2->SetMinimum(0);
   Graph_Graph2->SetMaximum(10.44726);
   Graph_Graph2->SetDirectory(0);
   Graph_Graph2->SetStats(0);

   ci = TColor::GetColor("#000099");
   Graph_Graph2->SetLineColor(ci);
   Graph_Graph2->GetXaxis()->SetLabelFont(42);
   Graph_Graph2->GetXaxis()->SetLabelSize(0.035);
   Graph_Graph2->GetXaxis()->SetTitleSize(0.035);
   Graph_Graph2->GetXaxis()->SetTitleFont(42);
   Graph_Graph2->GetYaxis()->SetLabelFont(42);
   Graph_Graph2->GetYaxis()->SetLabelSize(0.035);
   Graph_Graph2->GetYaxis()->SetTitleSize(0.035);
   Graph_Graph2->GetYaxis()->SetTitleFont(42);
   Graph_Graph2->GetZaxis()->SetLabelFont(42);
   Graph_Graph2->GetZaxis()->SetLabelSize(0.035);
   Graph_Graph2->GetZaxis()->SetTitleSize(0.035);
   Graph_Graph2->GetZaxis()->SetTitleFont(42);
   grae->SetHistogram(Graph_Graph2);
   
   grae->Draw("f");
   
   TGraph *graph = new TGraph(8);
   graph->SetName("Graph2");
   graph->SetTitle("Graph");
   graph->SetFillColor(1);

   ci = TColor::GetColor("#0000ff");
   graph->SetLineColor(ci);
   graph->SetLineStyle(2);
   graph->SetLineWidth(3);
   graph->SetPoint(0,4000,0.03900183304);
   graph->SetPoint(1,4500,0.0904257767);
   graph->SetPoint(2,5000,0.2011818797);
   graph->SetPoint(3,5500,0.4565734885);
   graph->SetPoint(4,6000,1.04789451);
   graph->SetPoint(5,6500,3.298884631);
   graph->SetPoint(6,7000,8.892705983);
   graph->SetPoint(7,7500,9.295764078);
   
   TH1F *Graph_Graph1 = new TH1F("Graph_Graph1","Graph",100,3650,7850);
   Graph_Graph1->SetMinimum(0);
   Graph_Graph1->SetMaximum(10.22144);
   Graph_Graph1->SetDirectory(0);
   Graph_Graph1->SetStats(0);

   ci = TColor::GetColor("#000099");
   Graph_Graph1->SetLineColor(ci);
   Graph_Graph1->GetXaxis()->SetLabelFont(42);
   Graph_Graph1->GetXaxis()->SetLabelSize(0.035);
   Graph_Graph1->GetXaxis()->SetTitleSize(0.035);
   Graph_Graph1->GetXaxis()->SetTitleFont(42);
   Graph_Graph1->GetYaxis()->SetLabelFont(42);
   Graph_Graph1->GetYaxis()->SetLabelSize(0.035);
   Graph_Graph1->GetYaxis()->SetTitleSize(0.035);
   Graph_Graph1->GetYaxis()->SetTitleFont(42);
   Graph_Graph1->GetZaxis()->SetLabelFont(42);
   Graph_Graph1->GetZaxis()->SetLabelSize(0.035);
   Graph_Graph1->GetZaxis()->SetTitleSize(0.035);
   Graph_Graph1->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_Graph1);
   
   graph->Draw("lp");
   
   graph = new TGraph(8);
   graph->SetName("Graph3");
   graph->SetTitle("Graph");
   graph->SetFillColor(1);
   graph->SetLineWidth(3);
   graph->SetPoint(0,4000,0.02599316818);
   graph->SetPoint(1,4500,0.0711020941);
   graph->SetPoint(2,5000,0.1750444324);
   graph->SetPoint(3,5500,0.3722666501);
   graph->SetPoint(4,6000,0.8647361806);
   graph->SetPoint(5,6500,2.683445921);
   graph->SetPoint(6,7000,8.389952982);
   graph->SetPoint(7,7500,9.00391915);
   
   TH1F *Graph_Graph2 = new TH1F("Graph_Graph2","Graph",100,3650,7850);
   Graph_Graph2->SetMinimum(0);
   Graph_Graph2->SetMaximum(9.901712);
   Graph_Graph2->SetDirectory(0);
   Graph_Graph2->SetStats(0);

   ci = TColor::GetColor("#000099");
   Graph_Graph2->SetLineColor(ci);
   Graph_Graph2->GetXaxis()->SetLabelFont(42);
   Graph_Graph2->GetXaxis()->SetLabelSize(0.035);
   Graph_Graph2->GetXaxis()->SetTitleSize(0.035);
   Graph_Graph2->GetXaxis()->SetTitleFont(42);
   Graph_Graph2->GetYaxis()->SetLabelFont(42);
   Graph_Graph2->GetYaxis()->SetLabelSize(0.035);
   Graph_Graph2->GetYaxis()->SetTitleSize(0.035);
   Graph_Graph2->GetYaxis()->SetTitleFont(42);
   Graph_Graph2->GetZaxis()->SetLabelFont(42);
   Graph_Graph2->GetZaxis()->SetLabelSize(0.035);
   Graph_Graph2->GetZaxis()->SetTitleSize(0.035);
   Graph_Graph2->GetZaxis()->SetTitleFont(42);
   graph->SetHistogram(Graph_Graph2);
   
   graph->Draw("pl");
   
   TPaveLabel *pl = new TPaveLabel(0.15,0.81,0.25,0.88,"CMS","NBNDC");
   pl->SetBorderSize(0);
   pl->SetFillColor(0);
   pl->SetFillStyle(0);
   pl->SetTextAlign(12);
   pl->SetTextSize(0.99);
   pl->Draw();
   
   TLegend *leg = new TLegend(0.15,0.473051,0.375,0.728644,NULL,"brNDC");
   leg->SetBorderSize(0);
   leg->SetTextSize(0.032);
   leg->SetLineColor(0);
   leg->SetLineStyle(0);
   leg->SetLineWidth(0);
   leg->SetFillColor(19);
   leg->SetFillStyle(0);
   TLegendEntry *entry=leg->AddEntry("NULL","ADD model","h");
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(42);
   entry=leg->AddEntry("Graph3","Obs. 95% CL limit","l");
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(3);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(42);
   entry=leg->AddEntry("Graph2","Exp. 95% CL limit, median","l");

   ci = TColor::GetColor("#0000ff");
   entry->SetLineColor(ci);
   entry->SetLineStyle(2);
   entry->SetLineWidth(3);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(42);
   entry=leg->AddEntry("Graph1","Exp. (68%)","f");

   ci = TColor::GetColor("#00cc00");
   entry->SetFillColor(ci);
   entry->SetFillStyle(1001);
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(42);
   entry=leg->AddEntry("Graph0","Exp. (95%)","f");

   ci = TColor::GetColor("#ffcc00");
   entry->SetFillColor(ci);
   entry->SetFillStyle(1001);
   entry->SetLineColor(1);
   entry->SetLineStyle(1);
   entry->SetLineWidth(1);
   entry->SetMarkerColor(1);
   entry->SetMarkerStyle(21);
   entry->SetMarkerSize(1);
   entry->SetTextFont(42);
   leg->Draw();
   
   pl = new TPaveLabel(0.4,0.905,0.9,0.99,"35.9 fb^{-1} (13 TeV, ee) + 36.3 fb^{-1} (13 TeV, #mu#mu)","NBNDC");
   pl->SetBorderSize(0);
   pl->SetFillColor(0);
   pl->SetTextFont(42);
   pl->SetTextSize(0.5);
   pl->Draw();
   TLine *line = new TLine(10,1,40,1);

   ci = TColor::GetColor("#ff0000");
   line->SetLineColor(ci);
   line->SetLineWidth(2);
   line->Draw();
   
   TH1F *DummyGraph = new TH1F("DummyGraph","",100,4000,7500);
   DummyGraph->SetMinimum(0);
   DummyGraph->SetMaximum(8);
   DummyGraph->SetDirectory(0);
   DummyGraph->SetStats(0);

   ci = TColor::GetColor("#000099");
   DummyGraph->SetLineColor(ci);
   DummyGraph->GetXaxis()->SetTitle("#Lambda [GeV]");
   DummyGraph->GetXaxis()->SetRange(1,100);
   DummyGraph->GetXaxis()->SetLabelFont(42);
   DummyGraph->GetXaxis()->SetTitleSize(0.045);
   DummyGraph->GetXaxis()->SetTitleFont(42);
   DummyGraph->GetYaxis()->SetTitle("95% CL limit on signal strength #mu");
   DummyGraph->GetYaxis()->SetLabelFont(42);
   DummyGraph->GetYaxis()->SetTitleSize(0.045);
   DummyGraph->GetYaxis()->SetTitleFont(42);
   DummyGraph->GetZaxis()->SetLabelFont(42);
   DummyGraph->GetZaxis()->SetLabelSize(0.035);
   DummyGraph->GetZaxis()->SetTitleSize(0.035);
   DummyGraph->GetZaxis()->SetTitleFont(42);
   DummyGraph->Draw("sameaxis");
   plotPad->Modified();
   cCL->cd();
   cCL->Modified();
   cCL->cd();
   cCL->SetSelected(cCL);
}
