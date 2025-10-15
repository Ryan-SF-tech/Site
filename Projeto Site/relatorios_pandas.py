import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
from app import create_app, db
from app.models.Usuario import Usuario
from app.models.administrador import Administrador
from app.models.centro_adocao import CentroAdocao
from app.models.produto import Produto, Venda, ItemVenda
from app.models.teste_aptidao import TesteAptidao


plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class RelatoriosPetAdocao:
    def __init__(self):
        self.app = create_app()
        
    def gerar_relatorio_usuarios(self):
        """Relatório de análise de usuários"""
        with self.app.app_context():
            usuarios = Usuario.query.all()
            
            if not usuarios:
                print("⚠️ Nenhum usuário encontrado no banco de dados")
                return None
            
            
            df_usuarios = pd.DataFrame([{
                'ID': u.id,
                'Nome': u.nome,
                'Email': u.email,
                'Data_Cadastro': getattr(u, 'data_cadastro', None)
            } for u in usuarios])
            
            print("=" * 60)
            print("📊 RELATÓRIO DE USUÁRIOS")
            print("=" * 60)
            
            
            print(f"👥 Total de usuários: {len(df_usuarios)}")
            print(f"📧 Domínios de email mais comuns:")
            dominios = df_usuarios['Email'].str.split('@').str[1].value_counts()
            print(dominios.head())
            
            return df_usuarios
    
    def gerar_relatorio_produtos(self):
        """Relatório de análise de produtos e vendas"""
        with self.app.app_context():
            produtos = Produto.query.all()
            vendas = Venda.query.all()
            itens_venda = ItemVenda.query.all()
            
            
            df_produtos = pd.DataFrame([{
                'ID': p.id,
                'Nome': p.nome,
                'Categoria': p.categoria,
                'Preco': p.preco,
                'Estoque': p.quantidade_estoque,
                'Data_Cadastro': p.data_cadastro
            } for p in produtos])
            
            
            df_vendas = pd.DataFrame([{
                'ID': v.id,
                'Data_Venda': v.data_venda,
                'Total': v.total,
                'Status': v.status
            } for v in vendas])
            
            
            df_itens = pd.DataFrame([{
                'ID': i.id,
                'Venda_ID': i.venda_id,
                'Produto_ID': i.produto_id,
                'Quantidade': i.quantidade,
                'Preco_Unitario': i.preco_unitario,
                'Subtotal': i.quantidade * i.preco_unitario
            } for i in itens_venda])
            
            print("\n" + "=" * 60)
            print("🛍️ RELATÓRIO DE PRODUTOS E VENDAS")
            print("=" * 60)
            
            
            if not df_produtos.empty:
                print(f"📦 Total de produtos: {len(df_produtos)}")
                print(f"💰 Preço médio: R$ {df_produtos['Preco'].mean():.2f}")
                print(f"📊 Estoque total: {df_produtos['Estoque'].sum()} unidades")
                
                
                produtos_por_categoria = df_produtos.groupby('Categoria').agg({
                    'ID': 'count',
                    'Preco': 'mean',
                    'Estoque': 'sum'
                }).rename(columns={'ID': 'Quantidade'})
                print("\n📈 Produtos por categoria:")
                print(produtos_por_categoria)
            
            
            if not df_vendas.empty:
                print(f"\n💳 Total de vendas: {len(df_vendas)}")
                print(f"💰 Valor total vendido: R$ {df_vendas['Total'].sum():.2f}")
                print(f"📈 Ticket médio: R$ {df_vendas['Total'].mean():.2f}")
                
                
                vendas_por_status = df_vendas['Status'].value_counts()
                print(f"\n📋 Vendas por status:")
                print(vendas_por_status)
            
            return {
                'produtos': df_produtos,
                'vendas': df_vendas,
                'itens_venda': df_itens
            }
    
    def gerar_relatorio_centros_adocao(self):
        """Relatório de análise de centros de adoção"""
        with self.app.app_context():
            centros = CentroAdocao.query.all()
            
            if not centros:
                print("⚠️ Nenhum centro de adoção encontrado")
                return None
            
            df_centros = pd.DataFrame([{
                'ID': c.id,
                'Nome': c.nome,
                'Endereco': c.endereco,
                'Latitude': c.latitude,
                'Longitude': c.longitude,
                'Telefone': c.telefone,
                'Website': c.website,
                'Data_Cadastro': c.data_cadastro
            } for c in centros])
            
            print("\n" + "=" * 60)
            print("🏠 RELATÓRIO DE CENTROS DE ADOÇÃO")
            print("=" * 60)
            
            print(f"📍 Total de centros cadastrados: {len(df_centros)}")
            
            
            if len(df_centros) > 1:
                print(f"🌍 Distribuição geográfica:")
                print(f"   Latitude: {df_centros['Latitude'].min():.4f} a {df_centros['Latitude'].max():.4f}")
                print(f"   Longitude: {df_centros['Longitude'].min():.4f} a {df_centros['Longitude'].max():.4f}")
            
            
            com_website = df_centros['Website'].notna().sum()
            print(f"🌐 Centros com website: {com_website}/{len(df_centros)}")
            
            return df_centros
    
    def gerar_relatorio_testes_aptidao(self):
        """Relatório de análise dos testes de aptidão"""
        with self.app.app_context():
            testes = TesteAptidao.query.all()
            
            if not testes:
                print("⚠️ Nenhum teste de aptidão encontrado")
                return None
            
            df_testes = pd.DataFrame([{
                'ID': t.id,
                'Nome_Usuario': t.nome_usuario,
                'Total_Sim': t.total_sim,
                'Data_Teste': t.data_teste,
                'Apto': '✅ SIM' if t.total_sim > 7 else '❌ NÃO'
            } for t in testes])
            
            print("\n" + "=" * 60)
            print("🎯 RELATÓRIO DE TESTES DE APTIDÃO")
            print("=" * 60)
            
            print(f"📝 Total de testes realizados: {len(df_testes)}")
            
            if not df_testes.empty:
                
                aptos = (df_testes['Total_Sim'] > 7).sum()
                nao_aptos = (df_testes['Total_Sim'] <= 7).sum()
                
                print(f"✅ Usuários aptos: {aptos} ({aptos/len(df_testes)*100:.1f}%)")
                print(f"❌ Usuários não aptos: {nao_aptos} ({nao_aptos/len(df_testes)*100:.1f}%)")
                print(f"📊 Média de respostas 'SIM': {df_testes['Total_Sim'].mean():.1f}/15")
                
                
                print(f"\n📈 Distribuição dos scores:")
                score_dist = df_testes['Total_Sim'].value_counts().sort_index()
                for score, count in score_dist.items():
                    print(f"   {score}/15: {count} usuários")
            
            return df_testes
    
    def criar_graficos(self, dados):
        """Cria gráficos visuais para o relatório"""
        try:
            fig, axes = plt.subplots(2, 2, figsize=(15, 12))
            fig.suptitle('📈 Dashboard PetAdocao - Análise Completa', fontsize=16, fontweight='bold')
            
            
            if 'produtos' in dados and not dados['produtos'].empty:
                produtos_por_cat = dados['produtos']['Categoria'].value_counts()
                axes[0,0].pie(produtos_por_cat.values, labels=produtos_por_cat.index, autopct='%1.1f%%')
                axes[0,0].set_title('📦 Distribuição de Produtos por Categoria')
            
            
            if 'testes' in dados and not dados['testes'].empty:
                aptos = (dados['testes']['Total_Sim'] > 7).value_counts()
                if len(aptos) > 0:
                    axes[0,1].bar(['Não Apto', 'Apto'], aptos.values, color=['red', 'green'])
                    axes[0,1].set_title('🎯 Resultados dos Testes de Aptidão')
                    axes[0,1].set_ylabel('Quantidade de Usuários')
            
            
            if 'vendas' in dados and not dados['vendas'].empty:
                vendas_status = dados['vendas']['Status'].value_counts()
                axes[1,0].bar(vendas_status.index, vendas_status.values)
                axes[1,0].set_title('💳 Vendas por Status')
                axes[1,0].tick_params(axis='x', rotation=45)
            
            
            if 'testes' in dados and not dados['testes'].empty:
                testes_por_mes = dados['testes'].groupby(
                    dados['testes']['Data_Teste'].dt.to_period('M')
                ).size()
                axes[1,1].plot(testes_por_mes.index.astype(str), testes_por_mes.values, marker='o')
                axes[1,1].set_title('📅 Testes Realizados por Mês')
                axes[1,1].tick_params(axis='x', rotation=45)
            
            plt.tight_layout()
            plt.savefig('relatorio_petadocao.png', dpi=300, bbox_inches='tight')
            print(f"\n📊 Gráficos salvos em: relatorio_petadocao.png")
            
        except Exception as e:
            print(f"⚠️ Erro ao criar gráficos: {e}")
    
    def exportar_para_excel(self, dados):
        """Exporta todos os dados para Excel"""
        try:
            with pd.ExcelWriter('relatorio_completo_petadocao.xlsx', engine='openpyxl') as writer:
                for nome, df in dados.items():
                    if df is not None and not df.empty:
                        df.to_excel(writer, sheet_name=nome[:31], index=False)
            
            print(f"📁 Relatório Excel salvo em: relatorio_completo_petadocao.xlsx")
        except Exception as e:
            print(f"⚠️ Erro ao exportar para Excel: {e}")
    
    def gerar_relatorio_completo(self):
        """Gera relatório completo consolidado"""
        print("🚀 INICIANDO GERAÇÃO DE RELATÓRIOS PETADOCAO")
        print("=" * 60)
        
        dados_completos = {}
        
        
        dados_completos['usuarios'] = self.gerar_relatorio_usuarios()
        dados_produtos = self.gerar_relatorio_produtos()
        if dados_produtos:
            dados_completos.update(dados_produtos)
        dados_completos['centros'] = self.gerar_relatorio_centros_adocao()
        dados_completos['testes'] = self.gerar_relatorio_testes_aptidao()
        
        
        dados_completos = {k: v for k, v in dados_completos.items() if v is not None}
        
        
        self.criar_graficos(dados_completos)
        
        
        self.exportar_para_excel(dados_completos)
        
        print("\n" + "=" * 60)
        print("✅ RELATÓRIO COMPLETO GERADO COM SUCESSO!")
        print("=" * 60)
        
        return dados_completos


if __name__ == "__main__":
    relatorios = RelatoriosPetAdocao()
    dados = relatorios.gerar_relatorio_completo()