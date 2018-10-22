2#Algoritmo genetico simples redigido por:
#Rafael Rodrigues
#Itallo Azevedo
#Jhoe Ohaze


import random
from datetime import datetime



class Populacao():
    def __init__(self):
        self.Individuo = list()
        self.tamPopulacao = 0


    def randomPop(self, numGenes, tamPop):

        self.tamPopulacao = tamPop
        for i in range(tamPop):
            random.seed(datetime.now())
            self.Individuo_Class = Individuo()
            self.Individuo.append(self.Individuo_Class.new_Individuo(numGenes))

        return

    def populacao_nula(self, tamPop):
        self.tamPopulacao = tamPop


        for i in range(self.tamPopulacao):
            self.Individuo.append(None)

    def setIndividuo(self, individuo, posicao):
        self.Individuo[posicao] = individuo

    def setIndividuoNext(self, individuo):

        for i in range(self.tamPopulacao):
            if self.Individuo[i] == None:
                self.Individuo[i] = individuo
                return

    def temSolucao(self, solucao):
        i = None
        for j in range(len(self.Individuo)):
            if self.Individuo[j].genes == solucao:
                i = self.Individuo[j]
                break
        if i == None:
            return False
        return i

    def ordenaPopulacao(self):
        trocou = True
        while trocou :
            trocou = False

            for i in range(len(self.Individuo)-1):

                if self.Individuo[i].aptidao < self.Individuo[i + 1].aptidao:

                    temp = self.Individuo[i]
                    self.Individuo[i] = self.Individuo[i + 1]
                    self.Individuo[i + 1] = temp
                    trocou  =  True


    def getNumIndividuos(self):
        return len(self.Individuo)

class Individuo():
    def __init__(self):
        self.genes = ''
        self.aptidao = 0
        self.Dados = Dados()
        self.numGenes = len(self.Dados.frase)

    def new_Individuo(self,numGenes):
        self.genes = ''
        characteres = self.Dados.characteres
        for i in range(self.numGenes):
            self.genes += characteres[random.randint(0,(len(characteres)-1))]
        self.geraAptidao()
        return self

    def Individuo(self,genes):
        self.genes = genes
        if random.uniform(0,1) <= self.Dados.taxaDeMutacao:
            characteres = self.Dados.characteres
            geneNovo = ''
            posAleatoria = random.randint(0,len(genes))
            for i in range(len(genes)):
                if i ==posAleatoria:
                    geneNovo += characteres[random.randint(0,len(characteres)-1)]
                else:
                    geneNovo += genes[i]
            self.genes = geneNovo
        self.geraAptidao()
        return

    def geraAptidao(self):
        solucao = self.Dados.frase

        for i in range(len(solucao)):
            if solucao[i] == self.genes[i]:
                self.aptidao+=1
        return

class Dados():

    def __init__(self):
        self.frase = 'Encoinfo' // HERE IS THE WORD THAT THIS AG WILL TRY TO FIND
        self.characteres = "!,.:;?áÁãÃâÂõÕôÔóÓéêÉÊíQWERTYUIOPASDFGHJKLÇZXCVBNMqwertyuiopasdfghjklçzxcvbnm1234567890 " # verificar na bilbioteca string se existe os caracteres la, dai é so importar
        self.taxaDeMutacao = 0.43
        return

    def novaGeracao(self,populacao,elitismo):



        novaPopulacao = Populacao()

        if elitismo:
            novaPopulacao.Individuo.append(populacao.Individuo[0])

        while novaPopulacao.getNumIndividuos() < len(populacao.Individuo):
            pais = self.selecaoTorneio(populacao)

            filhos =  self.crossover(pais[0], pais[1])
            novaPopulacao.Individuo.append(filhos[0])
            novaPopulacao.Individuo.append((filhos[1]))


        novaPopulacao.ordenaPopulacao()
        return novaPopulacao

    def crossover(self,individuo1,individuo2):
        pontoCorte1 = random.randint(0,(len(individuo1.genes)))
        while pontoCorte1 == 0 or pontoCorte1 == len(individuo1.genes):
            pontoCorte1 = random.randint(0,(len(individuo1.genes)))


        filhos = list()
        filhos.append(Individuo())
        filhos.append(Individuo())

        genePai1 = individuo1.genes
        genePai2 = individuo2.genes


        geneFilho1 = genePai1[:pontoCorte1]
        geneFilho1 += genePai2[pontoCorte1:len(genePai1)]

        geneFilho2 = genePai2[0: pontoCorte1]
        geneFilho2 += genePai1[pontoCorte1:len(genePai2)]


        filhos[0].Individuo(geneFilho1)
        filhos[1].Individuo(geneFilho2)


        return filhos

    def selecaoTorneio(self,populacao):
        populacaoIntermediaria = Populacao()
        populacaoIntermediaria.populacao_nula(3)

        populacaoIntermediaria.setIndividuoNext(populacao.Individuo[random.randint(0,len(populacao.Individuo)-1)])
        populacaoIntermediaria.setIndividuoNext(populacao.Individuo[random.randint(0,len(populacao.Individuo)-1)])
        populacaoIntermediaria.setIndividuoNext(populacao.Individuo[random.randint(0, len(populacao.Individuo) - 1)])

        populacaoIntermediaria.ordenaPopulacao()





        pais = list()

        pais.append(populacaoIntermediaria.Individuo[0])
        pais.append(populacaoIntermediaria.Individuo[1])

        return pais

def main():
    print('Iniciando Algoritmo genetico')
    dados = Dados()

    tamPop = 6

    numGenes = len(dados.frase)
    print('Criando populacao inicial')
    populacao = Populacao()
    populacao.randomPop(numGenes, tamPop)
    temSolucao = False
    geracao = 0

    while temSolucao == False:
        print('geracao: %d',geracao)
        geracao = geracao + 1
        print('Criando nova geracao a partir dos individuos mais aptos...')
        populacao = dados.novaGeracao(populacao, True)
        print('Individuo mais apto gerado: %s'%(populacao.Individuo[0].genes))
        print('Verificando se ha solucao')
        temSolucao = populacao.temSolucao(dados.frase)
        if temSolucao:
            print('Solucao: %s',temSolucao.genes)
            print( 'Solucao encontrada na geracao '+str(geracao))
            break
        print ('Solucao nao encontrada\n')

main()
